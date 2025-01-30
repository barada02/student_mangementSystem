from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure secret key

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    name = request.form['name']
    
    conn = sqlite3.connect('student_management.db')
    c = conn.cursor()
    
    try:
        c.execute('INSERT INTO admin_credentials (username, password, name) VALUES (?, ?, ?)',
                 (username, password, name))
        conn.commit()
        flash('Account created successfully! Please login.', 'success')
    except sqlite3.IntegrityError:
        flash('Username already exists!', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = sqlite3.connect('student_management.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM admin_credentials WHERE username = ? AND password = ?',
             (username, password))
    user = c.fetchone()
    conn.close()
    
    if user:
        session['user_id'] = user[0]
        session['username'] = user[1]
        session['name'] = user[3]
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password!', 'error')
        return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('base_dashboard.html', name=session.get('name'))

@app.route('/dashboard/<page>')
@login_required
def dashboard_content(page):
    if page == 'dashboard':
        # Get dashboard statistics
        conn = sqlite3.connect('student_management.db')
        c = conn.cursor()
        
        # Get total students
        c.execute('SELECT COUNT(*) FROM students')
        total_students = c.fetchone()[0]
        
        # Get total courses
        c.execute('SELECT COUNT(*) FROM courses')
        total_courses = c.fetchone()[0]
        
        # Get new enrollments (last 30 days)
        c.execute('SELECT COUNT(*) FROM enrollments WHERE date(enrollment_date) >= date("now", "-30 days")')
        new_enrollments = c.fetchone()[0]
        
        # Get students graduating soon (next 6 months)
        c.execute('SELECT COUNT(*) FROM students WHERE expected_leave_year = ? AND expected_leave_year IS NOT NULL', 
                 (datetime.now().year,))
        graduating_soon = c.fetchone()[0]
        
        # Get recent activities
        c.execute('''
            SELECT 'student' as type, name, date(enrollment_year) as date
            FROM students
            UNION ALL
            SELECT 'enrollment' as type, s.name, date(e.enrollment_date) as date
            FROM enrollments e
            JOIN students s ON e.student_id = s.id
            ORDER BY date DESC
            LIMIT 5
        ''')
        
        activities = []
        for row in c.fetchall():
            if row[0] == 'student':
                activities.append({
                    'icon': 'fas fa-user-plus',
                    'description': f'New student {row[1]} joined',
                    'time': row[2]
                })
            else:
                activities.append({
                    'icon': 'fas fa-book',
                    'description': f'Student {row[1]} enrolled in a course',
                    'time': row[2]
                })
        
        conn.close()
        
        stats = {
            'total_students': total_students,
            'total_courses': total_courses,
            'new_enrollments': new_enrollments,
            'graduating_soon': graduating_soon
        }
        
        return render_template('dashboard_content.html', stats=stats, activities=activities)
        
    elif page == 'students':
        # Get all students for the list view
        conn = sqlite3.connect('student_management.db')
        c = conn.cursor()
        c.execute('''
            SELECT id, name, email, category, enrollment_year, expected_leave_year 
            FROM students 
            ORDER BY name
        ''')
        students = [
            {
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'category': row[3],
                'enrollment_year': row[4],
                'expected_leave_year': row[5]
            }
            for row in c.fetchall()
        ]
        conn.close()
        return render_template('students_content.html', students=students)
        
    elif page == 'enrollment':
        # Return the enrollment form
        current_year = datetime.now().year
        current_date = datetime.now().strftime('%Y-%m-%d')
        return render_template('enrollment_content.html', 
                             current_year=current_year,
                             current_date=current_date)
        
    elif page == 'courses':
        return "Courses content coming soon"
        
    elif page == 'settings':
        return "Settings content coming soon"
        
    return "Content not found", 404

@app.route('/student_enrollment')
@login_required
def student_enrollment():
    return render_template('student_enrollment.html', name=session.get('name'))

@app.route('/enroll_student', methods=['POST'])
@login_required
def enroll_student():
    try:
        # Get form data
        name = request.form['name']
        email = request.form['email']
        dob = request.form['dob']
        category = request.form['category']
        special_identification = request.form['special_identification']
        enrollment_year = request.form['enrollment_year']
        expected_leave_year = request.form['expected_leave_year']
        
        # Connect to database
        conn = sqlite3.connect('student_management.db')
        c = conn.cursor()
        
        # Insert student data
        c.execute('''
            INSERT INTO students 
            (name, email, dob, category, special_identification, enrollment_year, expected_leave_year)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, email, dob, category, special_identification, enrollment_year, expected_leave_year))
        
        conn.commit()
        conn.close()
        
        flash('Student enrolled successfully!', 'success')
        return redirect(url_for('dashboard_content', page='students'))
        
    except sqlite3.IntegrityError:
        flash('Email already exists!', 'error')
        return redirect(url_for('dashboard_content', page='enrollment'))
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('dashboard_content', page='enrollment'))

@app.route('/delete_student/<int:id>', methods=['DELETE'])
@login_required
def delete_student(id):
    try:
        conn = sqlite3.connect('student_management.db')
        c = conn.cursor()
        
        # Delete student
        c.execute('DELETE FROM students WHERE id = ?', (id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from functools import wraps

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
    return render_template('dashboard.html', name=session.get('name'))

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
        return redirect(url_for('student_enrollment'))
        
    except sqlite3.IntegrityError:
        flash('Email already exists!', 'error')
        return redirect(url_for('student_enrollment'))
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('student_enrollment'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

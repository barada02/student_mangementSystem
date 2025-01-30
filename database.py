import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('student_management.db')
    c = conn.cursor()

    # Create Admin Credentials table
    c.execute('''
        CREATE TABLE IF NOT EXISTS admin_credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL
        )
    ''')

    # Create Students table
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            dob DATE NOT NULL,
            category TEXT NOT NULL CHECK(category IN ('Undergraduate', 'Postgraduate')),
            special_identification TEXT,
            enrollment_year INTEGER NOT NULL,
            expected_leave_year INTEGER NOT NULL
        )
    ''')

    # Create Courses table
    c.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            description TEXT
        )
    ''')

    # Create Enrollments table
    c.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            enrollment_date DATE NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (course_id) REFERENCES courses (id)
        )
    ''')

    # Insert a default admin account if it doesn't exist
    c.execute('''
        INSERT OR IGNORE INTO admin_credentials (username, password, name)
        VALUES (?, ?, ?)
    ''', ('admin', 'admin123', 'Administrator'))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!")

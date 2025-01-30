# Student Management System

A modern web-based student management system built with Flask and SQLite, featuring a responsive dashboard interface for managing student enrollments and courses.

## Features

### Authentication
- Secure login and signup system
- Session management for authenticated users
- Protected routes requiring authentication

### Dashboard
- Modern, responsive dashboard layout with sidebar navigation
- Real-time statistics display:
  - Total number of students
  - Total courses
  - New enrollments (last 30 days)
  - Students graduating soon
- Recent activity feed showing latest enrollments and updates

### Student Management
- Comprehensive student enrollment form with:
  - Personal information collection
  - Category selection (Undergraduate/Postgraduate)
  - Enrollment year and expected graduation year
  - Special identification notes
- Form validation:
  - Client-side validation for all required fields
  - Age verification (minimum 15 years)
  - Email uniqueness check
  - Study duration validation (maximum 6 years)
- Dynamic student list with:
  - Search functionality
  - View, edit, and delete actions
  - Responsive table layout

### User Interface
- Clean and modern design
- Responsive layout supporting mobile devices
- Interactive flash messages for user feedback
- Loading indicators for better UX
- Font Awesome icons for visual enhancement

## Technical Stack

### Backend
- Flask (Python web framework)
- SQLite database
- Flask session management
- RESTful routing

### Frontend
- HTML5
- CSS3 with modern features:
  - CSS Grid
  - Flexbox
  - Media queries for responsiveness
- JavaScript (ES6+)
  - Fetch API for AJAX requests
  - DOM manipulation
  - Form validation
- Font Awesome icons
- Google Fonts (Roboto)

## Database Schema

### Tables
1. admin_credentials
   - username (unique)
   - password
   - name

2. students
   - id (primary key)
   - name
   - email (unique)
   - dob
   - category
   - special_identification
   - enrollment_year
   - expected_leave_year

3. courses
   - id (primary key)
   - name
   - description

4. enrollments
   - id (primary key)
   - student_id (foreign key)
   - course_id (foreign key)
   - enrollment_date

## Recent Updates

### Authentication System
- Implemented secure login/signup functionality
- Added session management
- Created login/signup forms with validation

### Dashboard Development
- Created responsive dashboard layout
- Implemented sidebar navigation
- Added real-time statistics display
- Integrated recent activity feed

### Student Management
- Developed comprehensive enrollment form
- Added client-side and server-side validation
- Implemented student listing with search
- Added student deletion functionality
- Enhanced form submission with proper error handling and success notifications

### UI/UX Improvements
- Separated enrollment form and students list for better organization
- Added loading indicators during form submission
- Implemented flash messages for user feedback
- Enhanced mobile responsiveness
- Improved form styling and spacing

## Upcoming Features
- Course management implementation
- Student profile viewing and editing
- Advanced reporting system
- User settings and preferences
- File upload for student documents
- Email notifications

## Setup Instructions

1. Install Python dependencies:
```bash
pip install flask
```

2. Initialize the database:
```bash
python init_db.py
```

3. Run the application:
```bash
python app.py
```

4. Access the application at `http://localhost:5000`

## Contributing

This project is under active development. Feel free to submit issues and enhancement requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

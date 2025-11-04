# School Management System

A simple and efficient web-based school management system built with Flask and SQLite.

## Features

- **Student Management**: Add, view, update, and delete student records
- **Teacher Management**: Manage teacher profiles and information
- **Class Management**: Create and manage classes with schedules and room assignments
- **Attendance Tracking**: Record and monitor student attendance for all classes
- **Grade Management**: Record and manage student grades and assignments

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **ORM**: Flask-SQLAlchemy

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd school-management-system
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

### Students
- Navigate to the Students page to manage student records
- Click "Add New Student" to register a new student
- Use Edit/Delete buttons to modify or remove student records

### Teachers
- Navigate to the Teachers page to manage teacher profiles
- Click "Add New Teacher" to add a new teacher
- Update or remove teacher records as needed

### Classes
- Navigate to the Classes page to manage class schedules
- Click "Add New Class" to create a new class
- Assign teachers to classes and set schedules and room numbers

### Attendance
- Navigate to the Attendance page to record student attendance
- Click "Record Attendance" to mark a student's attendance for a specific class
- Select student, class, date, and status (Present, Absent, Late)

### Grades
- Navigate to the Grades page to manage student grades
- Click "Add Grade" to record a new grade
- Enter student, class, assignment name, grade, and date

## Database

The application uses SQLite database which will be automatically created when you first run the application. The database file `school.db` will be created in the project root directory.

### Database Schema

- **Students**: id, first_name, last_name, email, date_of_birth, enrollment_date, grade_level
- **Teachers**: id, first_name, last_name, email, subject, hire_date
- **Classes**: id, name, subject, teacher_id, schedule, room
- **Attendance**: id, student_id, class_id, date, status
- **Grades**: id, student_id, class_id, grade, assignment_name, date

## Project Structure

```
school-management-system/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── students.html
│   ├── teachers.html
│   ├── classes.html
│   ├── attendance.html
│   └── grades.html
└── static/               # Static files
    ├── css/
    │   └── style.css
    └── js/
        ├── students.js
        ├── teachers.js
        ├── classes.js
        ├── attendance.js
        └── grades.js
```

## API Endpoints

### Students
- GET `/api/students` - Get all students
- POST `/api/students` - Create a new student
- PUT `/api/students/<id>` - Update a student
- DELETE `/api/students/<id>` - Delete a student

### Teachers
- GET `/api/teachers` - Get all teachers
- POST `/api/teachers` - Create a new teacher
- PUT `/api/teachers/<id>` - Update a teacher
- DELETE `/api/teachers/<id>` - Delete a teacher

### Classes
- GET `/api/classes` - Get all classes
- POST `/api/classes` - Create a new class
- PUT `/api/classes/<id>` - Update a class
- DELETE `/api/classes/<id>` - Delete a class

### Attendance
- GET `/api/attendance` - Get all attendance records
- POST `/api/attendance` - Create an attendance record
- DELETE `/api/attendance/<id>` - Delete an attendance record

### Grades
- GET `/api/grades` - Get all grades
- POST `/api/grades` - Create a new grade
- PUT `/api/grades/<id>` - Update a grade
- DELETE `/api/grades/<id>` - Delete a grade

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

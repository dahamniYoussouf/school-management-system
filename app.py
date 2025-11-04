from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import db, Student, Teacher, Class, Attendance, Grade
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Student routes
@app.route('/students')
def students():
    return render_template('students.html')

@app.route('/api/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])

@app.route('/api/students', methods=['POST'])
def create_student():
    data = request.json
    try:
        student = Student(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date(),
            grade_level=data.get('grade_level', '')
        )
        db.session.add(student)
        db.session.commit()
        return jsonify(student.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.json
    try:
        student.first_name = data['first_name']
        student.last_name = data['last_name']
        student.email = data['email']
        student.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        student.grade_level = data.get('grade_level', '')
        db.session.commit()
        return jsonify(student.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return '', 204

# Teacher routes
@app.route('/teachers')
def teachers():
    return render_template('teachers.html')

@app.route('/api/teachers', methods=['GET'])
def get_teachers():
    teachers = Teacher.query.all()
    return jsonify([teacher.to_dict() for teacher in teachers])

@app.route('/api/teachers', methods=['POST'])
def create_teacher():
    data = request.json
    try:
        teacher = Teacher(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            subject=data.get('subject', '')
        )
        db.session.add(teacher)
        db.session.commit()
        return jsonify(teacher.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/teachers/<int:id>', methods=['PUT'])
def update_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    data = request.json
    try:
        teacher.first_name = data['first_name']
        teacher.last_name = data['last_name']
        teacher.email = data['email']
        teacher.subject = data.get('subject', '')
        db.session.commit()
        return jsonify(teacher.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/teachers/<int:id>', methods=['DELETE'])
def delete_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    db.session.delete(teacher)
    db.session.commit()
    return '', 204

# Class routes
@app.route('/classes')
def classes():
    return render_template('classes.html')

@app.route('/api/classes', methods=['GET'])
def get_classes():
    classes = Class.query.all()
    return jsonify([cls.to_dict() for cls in classes])

@app.route('/api/classes', methods=['POST'])
def create_class():
    data = request.json
    try:
        cls = Class(
            name=data['name'],
            subject=data['subject'],
            teacher_id=data['teacher_id'],
            schedule=data.get('schedule', ''),
            room=data.get('room', '')
        )
        db.session.add(cls)
        db.session.commit()
        return jsonify(cls.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/classes/<int:id>', methods=['PUT'])
def update_class(id):
    cls = Class.query.get_or_404(id)
    data = request.json
    try:
        cls.name = data['name']
        cls.subject = data['subject']
        cls.teacher_id = data['teacher_id']
        cls.schedule = data.get('schedule', '')
        cls.room = data.get('room', '')
        db.session.commit()
        return jsonify(cls.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/classes/<int:id>', methods=['DELETE'])
def delete_class(id):
    cls = Class.query.get_or_404(id)
    db.session.delete(cls)
    db.session.commit()
    return '', 204

# Attendance routes
@app.route('/attendance')
def attendance():
    return render_template('attendance.html')

@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    attendance_records = Attendance.query.all()
    return jsonify([record.to_dict() for record in attendance_records])

@app.route('/api/attendance', methods=['POST'])
def create_attendance():
    data = request.json
    try:
        attendance = Attendance(
            student_id=data['student_id'],
            class_id=data['class_id'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            status=data['status']
        )
        db.session.add(attendance)
        db.session.commit()
        return jsonify(attendance.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/attendance/<int:id>', methods=['DELETE'])
def delete_attendance(id):
    attendance = Attendance.query.get_or_404(id)
    db.session.delete(attendance)
    db.session.commit()
    return '', 204

# Grade routes
@app.route('/grades')
def grades():
    return render_template('grades.html')

@app.route('/api/grades', methods=['GET'])
def get_grades():
    grades = Grade.query.all()
    return jsonify([grade.to_dict() for grade in grades])

@app.route('/api/grades', methods=['POST'])
def create_grade():
    data = request.json
    try:
        grade = Grade(
            student_id=data['student_id'],
            class_id=data['class_id'],
            grade=data['grade'],
            assignment_name=data['assignment_name'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date()
        )
        db.session.add(grade)
        db.session.commit()
        return jsonify(grade.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/grades/<int:id>', methods=['PUT'])
def update_grade(id):
    grade = Grade.query.get_or_404(id)
    data = request.json
    try:
        grade.student_id = data['student_id']
        grade.class_id = data['class_id']
        grade.grade = data['grade']
        grade.assignment_name = data['assignment_name']
        grade.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        db.session.commit()
        return jsonify(grade.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/grades/<int:id>', methods=['DELETE'])
def delete_grade(id):
    grade = Grade.query.get_or_404(id)
    db.session.delete(grade)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

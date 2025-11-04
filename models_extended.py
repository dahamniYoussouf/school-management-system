from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

# ========================================
# MODULE 1: ADMINISTRATION GENERALE
# ========================================

class UserRole(str, Enum):
    ADMIN = "admin"
    DIRECTOR = "director"
    TEACHER = "teacher"
    STUDENT = "student"
    STAFF = "staff"
    PARENT = "parent"

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default=UserRole.STUDENT)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    profile_image = db.Column(db.String(255))
    language = db.Column(db.String(10), default='fr')
    two_factor_enabled = db.Column(db.Boolean, default=False)

    # Relationships
    permissions = db.relationship('UserPermission', backref='user', lazy=True, cascade='all, delete-orphan')
    audit_logs = db.relationship('AuditLog', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'language': self.language,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    module = db.Column(db.String(50))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'module': self.module
        }

class UserPermission(db.Model):
    __tablename__ = 'user_permissions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), nullable=False)
    granted_at = db.Column(db.DateTime, default=datetime.utcnow)

class SchoolSettings(db.Model):
    __tablename__ = 'school_settings'
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(200), nullable=False)
    logo_url = db.Column(db.String(255))
    primary_color = db.Column(db.String(7), default='#3498db')
    secondary_color = db.Column(db.String(7), default='#2ecc71')
    address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    website = db.Column(db.String(200))
    academic_year_start = db.Column(db.Date)
    academic_year_end = db.Column(db.Date)
    timezone = db.Column(db.String(50), default='UTC')

    def to_dict(self):
        return {
            'id': self.id,
            'school_name': self.school_name,
            'logo_url': self.logo_url,
            'primary_color': self.primary_color,
            'secondary_color': self.secondary_color,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'website': self.website
        }

class Campus(db.Model):
    __tablename__ = 'campuses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True)
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    is_active = db.Column(db.Boolean, default=True)

    departments = db.relationship('Department', backref='campus', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'address': self.address,
            'city': self.city,
            'country': self.country,
            'is_active': self.is_active
        }

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True)
    campus_id = db.Column(db.Integer, db.ForeignKey('campuses.id'))
    head_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.Text)

    programs = db.relationship('Program', backref='department', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'campus_id': self.campus_id,
            'description': self.description
        }

# ========================================
# MODULE 2: PEDAGOGIQUE
# ========================================

class Program(db.Model):
    __tablename__ = 'programs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(20), unique=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    level = db.Column(db.String(50))  # Bachelor, Master, Certificate
    duration_months = db.Column(db.Integer)
    credits = db.Column(db.Integer)
    description = db.Column(db.Text)
    objectives = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)

    courses = db.relationship('Course', backref='program', lazy=True)
    enrollments = db.relationship('Enrollment', backref='program', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'level': self.level,
            'duration_months': self.duration_months,
            'credits': self.credits,
            'description': self.description
        }

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(20), unique=True)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'))
    credits = db.Column(db.Integer)
    hours = db.Column(db.Integer)
    coefficient = db.Column(db.Float, default=1.0)
    description = db.Column(db.Text)
    syllabus = db.Column(db.Text)
    is_mandatory = db.Column(db.Boolean, default=True)

    classes = db.relationship('Class', backref='course', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'credits': self.credits,
            'hours': self.hours,
            'coefficient': self.coefficient,
            'is_mandatory': self.is_mandatory
        }

class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    semester = db.Column(db.String(20))
    academic_year = db.Column(db.String(20))
    max_students = db.Column(db.Integer)
    schedule = db.Column(db.Text)  # JSON format for complex schedules

    attendances = db.relationship('Attendance', backref='class_ref', lazy=True, cascade='all, delete-orphan')
    grades = db.relationship('Grade', backref='class_ref', lazy=True, cascade='all, delete-orphan')
    sessions = db.relationship('ClassSession', backref='class_ref', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'course_id': self.course_id,
            'teacher_id': self.teacher_id,
            'room_id': self.room_id,
            'semester': self.semester,
            'academic_year': self.academic_year,
            'max_students': self.max_students
        }

class ClassSession(db.Model):
    __tablename__ = 'class_sessions'
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    topic = db.Column(db.String(200))
    notes = db.Column(db.Text)
    materials = db.Column(db.Text)  # JSON format for file URLs
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled

    def to_dict(self):
        return {
            'id': self.id,
            'class_id': self.class_id,
            'date': self.date.strftime('%Y-%m-%d') if self.date else None,
            'start_time': self.start_time.strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None,
            'topic': self.topic,
            'status': self.status
        }

# ========================================
# MODULE 3: ETUDIANT
# ========================================

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    student_number = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10))
    nationality = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    emergency_contact = db.Column(db.String(100))
    emergency_phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    enrollment_date = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # active, suspended, graduated, dropped

    user = db.relationship('User', backref=db.backref('student_profile', uselist=False))
    enrollments = db.relationship('Enrollment', backref='student', lazy=True)
    attendances = db.relationship('Attendance', backref='student', lazy=True)
    grades = db.relationship('Grade', backref='student', lazy=True)
    documents = db.relationship('StudentDocument', backref='student', lazy=True)
    financial_records = db.relationship('StudentFinancial', backref='student', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'student_number': self.student_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.strftime('%Y-%m-%d') if self.date_of_birth else None,
            'email': self.user.email if self.user else None,
            'phone': self.phone,
            'status': self.status,
            'enrollment_date': self.enrollment_date.strftime('%Y-%m-%d') if self.enrollment_date else None
        }

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)
    enrollment_date = db.Column(db.Date, default=datetime.utcnow)
    expected_graduation = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')
    gpa = db.Column(db.Float)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'program_id': self.program_id,
            'enrollment_date': self.enrollment_date.strftime('%Y-%m-%d') if self.enrollment_date else None,
            'status': self.status,
            'gpa': self.gpa
        }

class StudentDocument(db.Model):
    __tablename__ = 'student_documents'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)  # transcript, certificate, cv, diploma
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'document_type': self.document_type,
            'file_name': self.file_name,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False)  # present, absent, late, excused
    notes = db.Column(db.Text)
    recorded_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'class_id': self.class_id,
            'date': self.date.strftime('%Y-%m-%d') if self.date else None,
            'status': self.status,
            'notes': self.notes
        }

class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    grade = db.Column(db.Float, nullable=False)
    assignment_name = db.Column(db.String(100), nullable=False)
    assignment_type = db.Column(db.String(50))  # exam, quiz, project, homework
    weight = db.Column(db.Float, default=1.0)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    comments = db.Column(db.Text)
    graded_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'class_id': self.class_id,
            'grade': self.grade,
            'assignment_name': self.assignment_name,
            'assignment_type': self.assignment_type,
            'weight': self.weight,
            'date': self.date.strftime('%Y-%m-%d') if self.date else None
        }

# ========================================
# MODULE 4: RH & ENSEIGNANTS
# ========================================

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    employee_number = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    hire_date = db.Column(db.Date, default=datetime.utcnow)
    specialization = db.Column(db.String(100))
    qualifications = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')  # active, on_leave, resigned, retired

    user = db.relationship('User', backref=db.backref('teacher_profile', uselist=False))
    classes = db.relationship('Class', backref='teacher', lazy=True)
    contracts = db.relationship('EmployeeContract', backref='teacher', lazy=True)
    evaluations = db.relationship('TeacherEvaluation', backref='teacher', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'employee_number': self.employee_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.user.email if self.user else None,
            'phone': self.phone,
            'specialization': self.specialization,
            'hire_date': self.hire_date.strftime('%Y-%m-%d') if self.hire_date else None,
            'status': self.status
        }

class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    employee_number = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(100))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    phone = db.Column(db.String(20))
    hire_date = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')

    user = db.relationship('User', backref=db.backref('staff_profile', uselist=False))
    contracts = db.relationship('EmployeeContract', backref='staff', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'employee_number': self.employee_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'position': self.position,
            'status': self.status
        }

class EmployeeContract(db.Model):
    __tablename__ = 'employee_contracts'
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    contract_type = db.Column(db.String(50), nullable=False)  # full-time, part-time, temporary, freelance
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    salary = db.Column(db.Float)
    currency = db.Column(db.String(10), default='EUR')
    work_hours = db.Column(db.Integer)
    contract_file = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'contract_type': self.contract_type,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'salary': self.salary,
            'is_active': self.is_active
        }

class TeacherEvaluation(db.Model):
    __tablename__ = 'teacher_evaluations'
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    evaluator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    evaluation_date = db.Column(db.Date, default=datetime.utcnow)
    rating = db.Column(db.Float)  # 1-5 scale
    comments = db.Column(db.Text)
    strengths = db.Column(db.Text)
    areas_for_improvement = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'evaluation_date': self.evaluation_date.strftime('%Y-%m-%d') if self.evaluation_date else None,
            'rating': self.rating,
            'comments': self.comments
        }

class Leave(db.Model):
    __tablename__ = 'leaves'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    leave_type = db.Column(db.String(50), nullable=False)  # sick, vacation, personal, maternity
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'leave_type': self.leave_type,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'status': self.status
        }

# ========================================
# MODULE 5: FINANCIER
# ========================================

class StudentFinancial(db.Model):
    __tablename__ = 'student_financial'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    academic_year = db.Column(db.String(20), nullable=False)
    total_fees = db.Column(db.Float, nullable=False)
    amount_paid = db.Column(db.Float, default=0.0)
    balance = db.Column(db.Float, default=0.0)
    currency = db.Column(db.String(10), default='EUR')
    payment_plan = db.Column(db.Text)  # JSON format
    status = db.Column(db.String(20), default='pending')  # pending, partial, paid, overdue

    payments = db.relationship('Payment', backref='student_financial', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'academic_year': self.academic_year,
            'total_fees': self.total_fees,
            'amount_paid': self.amount_paid,
            'balance': self.balance,
            'status': self.status
        }

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    student_financial_id = db.Column(db.Integer, db.ForeignKey('student_financial.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, default=datetime.utcnow)
    payment_method = db.Column(db.String(50))  # cash, card, bank_transfer, check
    transaction_id = db.Column(db.String(100), unique=True)
    receipt_number = db.Column(db.String(50), unique=True)
    notes = db.Column(db.Text)
    processed_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    invoice = db.relationship('Invoice', backref='payment', uselist=False)

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'payment_date': self.payment_date.strftime('%Y-%m-%d') if self.payment_date else None,
            'payment_method': self.payment_method,
            'transaction_id': self.transaction_id,
            'receipt_number': self.receipt_number
        }

class Invoice(db.Model):
    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable=False, unique=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    issue_date = db.Column(db.Date, default=datetime.utcnow)
    due_date = db.Column(db.Date)
    invoice_file = db.Column(db.String(500))

    def to_dict(self):
        return {
            'id': self.id,
            'invoice_number': self.invoice_number,
            'issue_date': self.issue_date.strftime('%Y-%m-%d') if self.issue_date else None,
            'due_date': self.due_date.strftime('%Y-%m-%d') if self.due_date else None
        }

class Scholarship(db.Model):
    __tablename__ = 'scholarships'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50))  # merit, need-based, sports, art
    criteria = db.Column(db.Text)
    available_slots = db.Column(db.Integer)
    academic_year = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)

    applications = db.relationship('ScholarshipApplication', backref='scholarship', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'amount': self.amount,
            'type': self.type,
            'available_slots': self.available_slots,
            'is_active': self.is_active
        }

class ScholarshipApplication(db.Model):
    __tablename__ = 'scholarship_applications'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    scholarship_id = db.Column(db.Integer, db.ForeignKey('scholarships.id'), nullable=False)
    application_date = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    documents = db.Column(db.Text)  # JSON format
    notes = db.Column(db.Text)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'scholarship_id': self.scholarship_id,
            'application_date': self.application_date.strftime('%Y-%m-%d') if self.application_date else None,
            'status': self.status
        }

# ========================================
# MODULE 6: INFRASTRUCTURE & LOGISTIQUE
# ========================================

class Building(db.Model):
    __tablename__ = 'buildings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    campus_id = db.Column(db.Integer, db.ForeignKey('campuses.id'))
    address = db.Column(db.Text)
    floors = db.Column(db.Integer)

    rooms = db.relationship('Room', backref='building', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'campus_id': self.campus_id,
            'floors': self.floors
        }

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    room_number = db.Column(db.String(20))
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'))
    room_type = db.Column(db.String(50))  # classroom, lab, auditorium, office
    capacity = db.Column(db.Integer)
    floor = db.Column(db.Integer)
    features = db.Column(db.Text)  # JSON format: projector, whiteboard, computers
    is_available = db.Column(db.Boolean, default=True)

    reservations = db.relationship('RoomReservation', backref='room', lazy=True)
    classes = db.relationship('Class', backref='room', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'room_number': self.room_number,
            'room_type': self.room_type,
            'capacity': self.capacity,
            'is_available': self.is_available
        }

class RoomReservation(db.Model):
    __tablename__ = 'room_reservations'
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    reserved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_name = db.Column(db.String(200))
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    purpose = db.Column(db.Text)
    status = db.Column(db.String(20), default='confirmed')  # pending, confirmed, cancelled

    def to_dict(self):
        return {
            'id': self.id,
            'room_id': self.room_id,
            'event_name': self.event_name,
            'start_datetime': self.start_datetime.isoformat() if self.start_datetime else None,
            'end_datetime': self.end_datetime.isoformat() if self.end_datetime else None,
            'status': self.status
        }

class Equipment(db.Model):
    __tablename__ = 'equipment'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    equipment_type = db.Column(db.String(50))
    serial_number = db.Column(db.String(100), unique=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    purchase_date = db.Column(db.Date)
    purchase_price = db.Column(db.Float)
    condition = db.Column(db.String(20), default='good')  # excellent, good, fair, poor
    maintenance_due = db.Column(db.Date)
    is_available = db.Column(db.Boolean, default=True)

    maintenance_records = db.relationship('MaintenanceRecord', backref='equipment', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'equipment_type': self.equipment_type,
            'serial_number': self.serial_number,
            'condition': self.condition,
            'is_available': self.is_available
        }

class MaintenanceRecord(db.Model):
    __tablename__ = 'maintenance_records'
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    maintenance_date = db.Column(db.Date, default=datetime.utcnow)
    maintenance_type = db.Column(db.String(50))  # repair, routine, inspection
    description = db.Column(db.Text)
    cost = db.Column(db.Float)
    performed_by = db.Column(db.String(100))

    def to_dict(self):
        return {
            'id': self.id,
            'equipment_id': self.equipment_id,
            'maintenance_date': self.maintenance_date.strftime('%Y-%m-%d') if self.maintenance_date else None,
            'maintenance_type': self.maintenance_type,
            'cost': self.cost
        }

class InventoryItem(db.Model):
    __tablename__ = 'inventory_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    sku = db.Column(db.String(50), unique=True)
    quantity = db.Column(db.Integer, default=0)
    unit = db.Column(db.String(20))
    reorder_level = db.Column(db.Integer, default=10)
    unit_price = db.Column(db.Float)
    supplier = db.Column(db.String(100))
    location = db.Column(db.String(100))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'sku': self.sku,
            'quantity': self.quantity,
            'unit_price': self.unit_price
        }

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    event_type = db.Column(db.String(50))  # conference, workshop, open_house, fashion_show
    description = db.Column(db.Text)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    max_participants = db.Column(db.Integer)
    is_public = db.Column(db.Boolean, default=False)
    registration_required = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='scheduled')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'event_type': self.event_type,
            'description': self.description,
            'start_datetime': self.start_datetime.isoformat() if self.start_datetime else None,
            'end_datetime': self.end_datetime.isoformat() if self.end_datetime else None,
            'is_public': self.is_public,
            'status': self.status
        }

# ========================================
# MODULE 7: COMMUNICATION & MARKETING
# ========================================

class Lead(db.Model):
    __tablename__ = 'leads'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    country = db.Column(db.String(100))
    interested_program = db.Column(db.String(200))
    source = db.Column(db.String(50))  # website, referral, social_media, event
    status = db.Column(db.String(20), default='new')  # new, contacted, qualified, converted, lost
    notes = db.Column(db.Text)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_contact = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'interested_program': self.interested_program,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    campaign_type = db.Column(db.String(50))  # email, social_media, event, advertising
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    budget = db.Column(db.Float)
    target_audience = db.Column(db.String(200))
    status = db.Column(db.String(20), default='draft')  # draft, active, paused, completed
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'campaign_type': self.campaign_type,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'status': self.status
        }

class Alumni(db.Model):
    __tablename__ = 'alumni'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, unique=True)
    graduation_year = db.Column(db.Integer, nullable=False)
    degree = db.Column(db.String(100))
    current_company = db.Column(db.String(200))
    current_position = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    linkedin_url = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    willing_to_mentor = db.Column(db.Boolean, default=False)

    student = db.relationship('Student', backref=db.backref('alumni_profile', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'graduation_year': self.graduation_year,
            'degree': self.degree,
            'current_company': self.current_company,
            'current_position': self.current_position,
            'is_active': self.is_active
        }

class Partner(db.Model):
    __tablename__ = 'partners'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50))  # corporate, academic, industry
    industry = db.Column(db.String(100))
    contact_person = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    website = db.Column(db.String(200))
    partnership_type = db.Column(db.String(100))  # internship, sponsorship, collaboration
    start_date = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'contact_person': self.contact_person,
            'email': self.email,
            'partnership_type': self.partnership_type,
            'is_active': self.is_active
        }

class Newsletter(db.Model):
    __tablename__ = 'newsletters'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    send_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='draft')  # draft, scheduled, sent
    recipients_count = db.Column(db.Integer)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'send_date': self.send_date.isoformat() if self.send_date else None,
            'status': self.status,
            'recipients_count': self.recipients_count
        }

# ========================================
# MODULE 8: REPORTING & BI
# ========================================

class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    report_type = db.Column(db.String(50))  # financial, academic, hr, operational
    description = db.Column(db.Text)
    parameters = db.Column(db.Text)  # JSON format
    file_path = db.Column(db.String(500))
    generated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'report_type': self.report_type,
            'generated_at': self.generated_at.isoformat() if self.generated_at else None
        }

class Dashboard(db.Model):
    __tablename__ = 'dashboards'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    config = db.Column(db.Text)  # JSON format with widget configurations
    is_default = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'is_default': self.is_default
        }

# ========================================
# MODULE 9: SECURITE & CONFORMITE
# ========================================

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(100), nullable=False)
    entity_type = db.Column(db.String(50))
    entity_id = db.Column(db.Integer)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.Text)  # JSON format

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'entity_type': self.entity_type,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

class GDPRConsent(db.Model):
    __tablename__ = 'gdpr_consents'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    consent_type = db.Column(db.String(50), nullable=False)  # data_processing, marketing, analytics
    consented = db.Column(db.Boolean, default=False)
    consent_date = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'consent_type': self.consent_type,
            'consented': self.consented,
            'consent_date': self.consent_date.isoformat() if self.consent_date else None
        }

class DataBackup(db.Model):
    __tablename__ = 'data_backups'
    id = db.Column(db.Integer, primary_key=True)
    backup_name = db.Column(db.String(200), nullable=False)
    backup_type = db.Column(db.String(50))  # full, incremental
    file_path = db.Column(db.String(500))
    file_size = db.Column(db.BigInteger)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='completed')

    def to_dict(self):
        return {
            'id': self.id,
            'backup_name': self.backup_name,
            'backup_type': self.backup_type,
            'file_size': self.file_size,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'status': self.status
        }

# ========================================
# MODULE 10: MOBILE & UX
# ========================================

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50))  # info, warning, success, error
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    link = db.Column(db.String(500))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'notification_type': self.notification_type,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class UserPreference(db.Model):
    __tablename__ = 'user_preferences'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    theme = db.Column(db.String(20), default='light')  # light, dark
    language = db.Column(db.String(10), default='fr')
    notifications_enabled = db.Column(db.Boolean, default=True)
    email_notifications = db.Column(db.Boolean, default=True)
    push_notifications = db.Column(db.Boolean, default=True)
    timezone = db.Column(db.String(50), default='UTC')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'theme': self.theme,
            'language': self.language,
            'notifications_enabled': self.notifications_enabled
        }

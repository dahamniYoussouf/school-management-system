from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_cors import CORS
from models_extended import *
from datetime import datetime, timedelta
import os
from functools import wraps

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school_integrated.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
CORS(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Permission decorator
def permission_required(permission_name):
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if not has_permission(current_user, permission_name):
                return jsonify({'error': 'Permission denied'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def has_permission(user, permission_name):
    """Check if user has specific permission"""
    if user.role == UserRole.ADMIN:
        return True
    return any(up.permission.name == permission_name for up in user.permissions)

# Create tables
with app.app_context():
    db.create_all()

    # Create default admin user if not exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@school.com',
            role=UserRole.ADMIN,
            language='fr'
        )
        admin.set_password('admin123')
        db.session.add(admin)

        # Create default school settings
        settings = SchoolSettings(
            school_name='École de Luxe et Design',
            email='info@school.com',
            phone='+33 1 23 45 67 89',
            primary_color='#3498db',
            secondary_color='#2ecc71'
        )
        db.session.add(settings)
        db.session.commit()
        print("Default admin user created: admin/admin123")

# ========================================
# AUTHENTICATION ROUTES
# ========================================

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get('username')).first()

    if user and user.check_password(data.get('password')):
        if not user.is_active:
            return jsonify({'error': 'Account is inactive'}), 403

        login_user(user)
        user.last_login = datetime.utcnow()
        db.session.commit()

        # Log audit
        log = AuditLog(
            user_id=user.id,
            action='login',
            entity_type='user',
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        db.session.add(log)
        db.session.commit()

        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict()
        })

    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    # Log audit
    log = AuditLog(
        user_id=current_user.id,
        action='logout',
        entity_type='user',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()

    logout_user()
    return jsonify({'message': 'Logout successful'})

@app.route('/api/auth/me', methods=['GET'])
@login_required
def get_current_user():
    return jsonify(current_user.to_dict())

# ========================================
# MODULE 1: ADMINISTRATION GENERALE
# ========================================

@app.route('/api/users', methods=['GET'])
@login_required
@permission_required('view_users')
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/api/users', methods=['POST'])
@login_required
@permission_required('create_users')
def create_user():
    data = request.json
    try:
        user = User(
            username=data['username'],
            email=data['email'],
            role=data.get('role', UserRole.STUDENT),
            language=data.get('language', 'fr')
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/settings', methods=['GET'])
@login_required
def get_settings():
    settings = SchoolSettings.query.first()
    return jsonify(settings.to_dict() if settings else {})

@app.route('/api/settings', methods=['PUT'])
@login_required
@permission_required('manage_settings')
def update_settings():
    settings = SchoolSettings.query.first()
    if not settings:
        settings = SchoolSettings()
        db.session.add(settings)

    data = request.json
    for key, value in data.items():
        if hasattr(settings, key):
            setattr(settings, key, value)

    db.session.commit()
    return jsonify(settings.to_dict())

@app.route('/api/campuses', methods=['GET'])
def get_campuses():
    campuses = Campus.query.all()
    return jsonify([campus.to_dict() for campus in campuses])

@app.route('/api/departments', methods=['GET'])
def get_departments():
    departments = Department.query.all()
    return jsonify([dept.to_dict() for dept in departments])

# ========================================
# MODULE 2: PEDAGOGIQUE
# ========================================

@app.route('/api/programs', methods=['GET'])
def get_programs():
    programs = Program.query.all()
    return jsonify([program.to_dict() for program in programs])

@app.route('/api/programs', methods=['POST'])
@login_required
@permission_required('manage_programs')
def create_program():
    data = request.json
    try:
        program = Program(
            name=data['name'],
            code=data['code'],
            department_id=data.get('department_id'),
            level=data.get('level'),
            duration_months=data.get('duration_months'),
            credits=data.get('credits'),
            description=data.get('description')
        )
        db.session.add(program)
        db.session.commit()
        return jsonify(program.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([course.to_dict() for course in courses])

@app.route('/api/courses', methods=['POST'])
@login_required
@permission_required('manage_courses')
def create_course():
    data = request.json
    try:
        course = Course(
            name=data['name'],
            code=data['code'],
            program_id=data.get('program_id'),
            credits=data.get('credits'),
            hours=data.get('hours'),
            coefficient=data.get('coefficient', 1.0),
            description=data.get('description')
        )
        db.session.add(course)
        db.session.commit()
        return jsonify(course.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/classes', methods=['GET'])
def get_classes():
    classes = Class.query.all()
    return jsonify([cls.to_dict() for cls in classes])

@app.route('/api/classes', methods=['POST'])
@login_required
@permission_required('manage_classes')
def create_class():
    data = request.json
    try:
        cls = Class(
            name=data['name'],
            course_id=data['course_id'],
            teacher_id=data['teacher_id'],
            room_id=data.get('room_id'),
            semester=data.get('semester'),
            academic_year=data.get('academic_year'),
            max_students=data.get('max_students')
        )
        db.session.add(cls)
        db.session.commit()
        return jsonify(cls.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# ========================================
# MODULE 3: ETUDIANT
# ========================================

@app.route('/api/students', methods=['GET'])
@login_required
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])

@app.route('/api/students/<int:id>', methods=['GET'])
@login_required
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify(student.to_dict())

@app.route('/api/students', methods=['POST'])
@login_required
@permission_required('manage_students')
def create_student():
    data = request.json
    try:
        # Create user account
        user = User(
            username=data['email'].split('@')[0],
            email=data['email'],
            role=UserRole.STUDENT,
            language=data.get('language', 'fr')
        )
        user.set_password(data.get('password', 'student123'))
        db.session.add(user)
        db.session.flush()

        # Create student profile
        student = Student(
            user_id=user.id,
            student_number=data['student_number'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date(),
            gender=data.get('gender'),
            nationality=data.get('nationality'),
            phone=data.get('phone'),
            address=data.get('address'),
            city=data.get('city'),
            country=data.get('country')
        )
        db.session.add(student)
        db.session.commit()
        return jsonify(student.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/students/<int:id>/documents', methods=['GET'])
@login_required
def get_student_documents(id):
    documents = StudentDocument.query.filter_by(student_id=id).all()
    return jsonify([doc.to_dict() for doc in documents])

@app.route('/api/attendance', methods=['GET'])
@login_required
def get_attendance():
    records = Attendance.query.all()
    return jsonify([record.to_dict() for record in records])

@app.route('/api/attendance', methods=['POST'])
@login_required
@permission_required('manage_attendance')
def create_attendance():
    data = request.json
    try:
        attendance = Attendance(
            student_id=data['student_id'],
            class_id=data['class_id'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            status=data['status'],
            notes=data.get('notes'),
            recorded_by=current_user.id
        )
        db.session.add(attendance)
        db.session.commit()
        return jsonify(attendance.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/grades', methods=['GET'])
@login_required
def get_grades():
    grades = Grade.query.all()
    return jsonify([grade.to_dict() for grade in grades])

@app.route('/api/grades', methods=['POST'])
@login_required
@permission_required('manage_grades')
def create_grade():
    data = request.json
    try:
        grade = Grade(
            student_id=data['student_id'],
            class_id=data['class_id'],
            grade=data['grade'],
            assignment_name=data['assignment_name'],
            assignment_type=data.get('assignment_type'),
            weight=data.get('weight', 1.0),
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            comments=data.get('comments'),
            graded_by=current_user.id
        )
        db.session.add(grade)
        db.session.commit()
        return jsonify(grade.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# ========================================
# MODULE 4: RH & ENSEIGNANTS
# ========================================

@app.route('/api/teachers', methods=['GET'])
@login_required
def get_teachers():
    teachers = Teacher.query.all()
    return jsonify([teacher.to_dict() for teacher in teachers])

@app.route('/api/teachers', methods=['POST'])
@login_required
@permission_required('manage_teachers')
def create_teacher():
    data = request.json
    try:
        # Create user account
        user = User(
            username=data['email'].split('@')[0],
            email=data['email'],
            role=UserRole.TEACHER,
            language=data.get('language', 'fr')
        )
        user.set_password(data.get('password', 'teacher123'))
        db.session.add(user)
        db.session.flush()

        # Create teacher profile
        teacher = Teacher(
            user_id=user.id,
            employee_number=data['employee_number'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date() if data.get('date_of_birth') else None,
            gender=data.get('gender'),
            phone=data.get('phone'),
            address=data.get('address'),
            specialization=data.get('specialization')
        )
        db.session.add(teacher)
        db.session.commit()
        return jsonify(teacher.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/staff', methods=['GET'])
@login_required
@permission_required('view_staff')
def get_staff():
    staff = Staff.query.all()
    return jsonify([s.to_dict() for s in staff])

@app.route('/api/leaves', methods=['GET'])
@login_required
def get_leaves():
    leaves = Leave.query.all()
    return jsonify([leave.to_dict() for leave in leaves])

@app.route('/api/leaves', methods=['POST'])
@login_required
def create_leave():
    data = request.json
    try:
        leave = Leave(
            employee_id=current_user.id,
            leave_type=data['leave_type'],
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
            reason=data.get('reason')
        )
        db.session.add(leave)
        db.session.commit()
        return jsonify(leave.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# ========================================
# MODULE 5: FINANCIER
# ========================================

@app.route('/api/financial/students', methods=['GET'])
@login_required
@permission_required('view_financial')
def get_student_financial():
    records = StudentFinancial.query.all()
    return jsonify([record.to_dict() for record in records])

@app.route('/api/payments', methods=['GET'])
@login_required
@permission_required('view_financial')
def get_payments():
    payments = Payment.query.all()
    return jsonify([payment.to_dict() for payment in payments])

@app.route('/api/payments', methods=['POST'])
@login_required
@permission_required('manage_payments')
def create_payment():
    data = request.json
    try:
        payment = Payment(
            student_financial_id=data['student_financial_id'],
            amount=data['amount'],
            payment_date=datetime.strptime(data['payment_date'], '%Y-%m-%d').date(),
            payment_method=data['payment_method'],
            transaction_id=data.get('transaction_id'),
            processed_by=current_user.id
        )
        db.session.add(payment)

        # Update student financial record
        financial = StudentFinancial.query.get(data['student_financial_id'])
        if financial:
            financial.amount_paid += data['amount']
            financial.balance = financial.total_fees - financial.amount_paid
            if financial.balance == 0:
                financial.status = 'paid'
            elif financial.amount_paid > 0:
                financial.status = 'partial'

        db.session.commit()
        return jsonify(payment.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/scholarships', methods=['GET'])
def get_scholarships():
    scholarships = Scholarship.query.filter_by(is_active=True).all()
    return jsonify([scholarship.to_dict() for scholarship in scholarships])

# ========================================
# MODULE 6: INFRASTRUCTURE & LOGISTIQUE
# ========================================

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    return jsonify([room.to_dict() for room in rooms])

@app.route('/api/rooms/available', methods=['GET'])
def get_available_rooms():
    date = request.args.get('date')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    # Simple availability check (can be enhanced)
    rooms = Room.query.filter_by(is_available=True).all()
    return jsonify([room.to_dict() for room in rooms])

@app.route('/api/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events])

@app.route('/api/equipment', methods=['GET'])
@login_required
def get_equipment():
    equipment = Equipment.query.all()
    return jsonify([eq.to_dict() for eq in equipment])

# ========================================
# MODULE 7: COMMUNICATION & MARKETING
# ========================================

@app.route('/api/leads', methods=['GET'])
@login_required
@permission_required('view_leads')
def get_leads():
    leads = Lead.query.all()
    return jsonify([lead.to_dict() for lead in leads])

@app.route('/api/leads', methods=['POST'])
def create_lead():
    """Public endpoint for lead capture"""
    data = request.json
    try:
        lead = Lead(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data.get('phone'),
            country=data.get('country'),
            interested_program=data.get('interested_program'),
            source=data.get('source', 'website')
        )
        db.session.add(lead)
        db.session.commit()
        return jsonify(lead.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/alumni', methods=['GET'])
def get_alumni():
    alumni = Alumni.query.filter_by(is_active=True).all()
    return jsonify([alum.to_dict() for alum in alumni])

@app.route('/api/partners', methods=['GET'])
def get_partners():
    partners = Partner.query.filter_by(is_active=True).all()
    return jsonify([partner.to_dict() for partner in partners])

# ========================================
# MODULE 8: REPORTING & BI
# ========================================

@app.route('/api/dashboard/stats', methods=['GET'])
@login_required
def get_dashboard_stats():
    """Get key statistics for dashboard"""
    stats = {
        'total_students': Student.query.filter_by(status='active').count(),
        'total_teachers': Teacher.query.filter_by(status='active').count(),
        'total_programs': Program.query.filter_by(is_active=True).count(),
        'total_courses': Course.query.count(),
        'active_classes': Class.query.filter_by(academic_year='2024-2025').count(),
        'pending_payments': StudentFinancial.query.filter(
            StudentFinancial.balance > 0
        ).count()
    }
    return jsonify(stats)

@app.route('/api/reports', methods=['GET'])
@login_required
@permission_required('view_reports')
def get_reports():
    reports = Report.query.all()
    return jsonify([report.to_dict() for report in reports])

# ========================================
# MODULE 9: SECURITE & CONFORMITE
# ========================================

@app.route('/api/audit-logs', methods=['GET'])
@login_required
@permission_required('view_audit_logs')
def get_audit_logs():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(100).all()
    return jsonify([log.to_dict() for log in logs])

@app.route('/api/gdpr/consent', methods=['POST'])
@login_required
def update_gdpr_consent():
    data = request.json
    try:
        consent = GDPRConsent(
            user_id=current_user.id,
            consent_type=data['consent_type'],
            consented=data['consented'],
            ip_address=request.remote_addr
        )
        db.session.add(consent)
        db.session.commit()
        return jsonify(consent.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# ========================================
# MODULE 10: MOBILE & UX
# ========================================

@app.route('/api/notifications', methods=['GET'])
@login_required
def get_notifications():
    notifications = Notification.query.filter_by(
        user_id=current_user.id
    ).order_by(Notification.created_at.desc()).limit(50).all()
    return jsonify([notif.to_dict() for notif in notifications])

@app.route('/api/notifications/<int:id>/read', methods=['PUT'])
@login_required
def mark_notification_read(id):
    notification = Notification.query.get_or_404(id)
    if notification.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    notification.is_read = True
    db.session.commit()
    return jsonify(notification.to_dict())

@app.route('/api/preferences', methods=['GET'])
@login_required
def get_preferences():
    preferences = UserPreference.query.filter_by(user_id=current_user.id).first()
    return jsonify(preferences.to_dict() if preferences else {})

@app.route('/api/preferences', methods=['PUT'])
@login_required
def update_preferences():
    preferences = UserPreference.query.filter_by(user_id=current_user.id).first()
    if not preferences:
        preferences = UserPreference(user_id=current_user.id)
        db.session.add(preferences)

    data = request.json
    for key, value in data.items():
        if hasattr(preferences, key):
            setattr(preferences, key, value)

    db.session.commit()
    return jsonify(preferences.to_dict())

# ========================================
# MAIN ROUTES
# ========================================

@app.route('/')
def index():
    return render_template('index_integrated.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

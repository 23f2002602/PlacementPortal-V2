import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from tasks import send_registration_email
from models import db, User, Company, Student
from auth import create_token

auth_bp = Blueprint('auth', __name__)


# ----------------------------
# Allowed file type check
# ----------------------------
def allowed_file(filename):
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    return ext in current_app.config.get('ALLOWED_EXTENSIONS', {'pdf'})

# =====================================================
# REGISTER
# =====================================================
@auth_bp.route('/register', methods=['POST'])
def register():

    data = request.form

    # Debug (remove later)
    print("FORM DATA:", request.form)
    print("FILES:", request.files)

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not name or not email or not password or not role:
        return jsonify({'error': 'name, email, password and role are required'}), 400

    if role not in ['student', 'company']:
        return jsonify({'error': 'role must be student or company'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    resume_file = None

    # ------------------------
    # STUDENT VALIDATION
    # ------------------------
    if role == 'student':

        if 'resume' not in request.files:
            return jsonify({'error': 'Resume PDF required'}), 400

        resume_file = request.files['resume']

        if resume_file.filename == '':
            return jsonify({'error': 'Resume file missing'}), 400

        if not allowed_file(resume_file.filename):
            return jsonify({'error': 'Only PDF files allowed'}), 400

        # File size check
        resume_file.seek(0, os.SEEK_END)
        size = resume_file.tell()

        if size > current_app.config.get('MAX_CONTENT_LENGTH', 5 * 1024 * 1024):
            return jsonify({'error': 'Resume too large (max 5MB)'}), 400

        resume_file.seek(0)

    # ------------------------
    # CREATE USER
    # ------------------------
    user = User(
        name=name,
        email=email,
        password=generate_password_hash(password),
        role=role
    )

    db.session.add(user)
    db.session.flush()

    # ------------------------
    # COMPANY PROFILE
    # ------------------------
    if role == 'company':

        company = Company(
            user_id=user.id,
            company_name=data.get('company_name', ''),
            description=data.get('description', ''),
            industry=data.get('industry', ''),
            hr_contact=data.get('hr_contact', ''),
            location=data.get('location', ''),
            website=data.get('website', '')
        )

        db.session.add(company)

    # ------------------------
    # STUDENT PROFILE
    # ------------------------
    elif role == 'student':

        student = Student(
            user_id=user.id,
            roll_number=data.get('roll_number', ''),
            branch=data.get('branch', ''),
            cgpa=float(data.get('cgpa', 0)),
            year=int(data.get('year', 1)),
            phone=data.get('phone', ''),
            skills=data.get('skills', ''),
            experience=data.get('experience', '')
        )

        db.session.add(student)
        db.session.flush()

        if resume_file:

            filename = f"{student.id}_{secure_filename(resume_file.filename)}"

            upload_dir = current_app.config.get('UPLOAD_FOLDER', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)

            filepath = os.path.join(upload_dir, filename)

            resume_file.save(filepath)

            student.resume_filename = filename

    db.session.commit()

    send_registration_email.delay(user.email, user.name)

    return jsonify({'message': 'Registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    if not data:
        return jsonify({'error': 'JSON body required'}), 400

    user = User.query.filter_by(email=data.get('email')).first()

    if not user or not check_password_hash(user.password, data.get('password')):
        return jsonify({'error': 'Invalid email or password'}), 401

    if not user.is_active:
        return jsonify({'error': 'Account is deactivated'}), 403

    token = create_token(user.id, user.role)

    response = {
        "token": token,
        "role": user.role,
        "name": user.name,
        "id": user.id
    }

    if user.role == 'company':
        company = Company.query.filter_by(user_id=user.id).first()
        if company and company.approval_status != "approved":
            return jsonify({"error": "Company awaiting admin approval"}), 403

    elif user.role == 'student':
        student = Student.query.filter_by(user_id=user.id).first()
        if student:
            response["student_id"] = student.id

    return jsonify(response), 200
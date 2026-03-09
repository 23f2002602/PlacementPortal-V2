import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, User, Company, Student
from auth import create_token

auth_bp = Blueprint('auth', __name__)

def allowed_file(filename):
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    return ext in current_app.config['ALLOWED_EXTENSIONS']

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data.get('name') or not data.get('email') or not data.get('password') or not data.get('role'):
        return jsonify({'error': 'name, email, password and role are required'}), 400
    
    if data['role'] not in ['student', 'company']:
        return jsonify({'error': 'role must be either student or company'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    if data['role'] == 'student':
        if 'resume' not in request.files or request.files['resume'].filename == '':
            return jsonify({'error': 'Resume PDF is required for student registration'}), 400

        resume_file = request.files['resume']

        if not allowed_file(resume_file.filename):
            return jsonify({'error': 'Only PDF files are allowed for resume'}), 400

        if len(resume_file.read()) > current_app.config['MAX_CONTENT_LENGTH']:
            return jsonify({'error': 'Resume file too large. Max 5 MB.'}), 400

        resume_file.seek(0)

    user = User(
        name = data['name'],
        email = data['email'],
        password = generate_password_hash(data['password']),
        role = data['role']
    )
    db.session.add(user)
    db.session.flush()

    #role=specific profile
    if data['role'] == 'company':
        company = Company(
            user_id = user.id,
            company_name = data.get('company_name', ''),
            description = data.get('description', ''),
            hr_contact = data.get('hr_contact', ''),
            website = data.get('website', '')
        )
        db.session.add(company)
        db.session.commit()
    
    elif data['role'] == 'student':
        student = Student(
            user_id = user.id,
            branch = data.get('branch', ''),
            roll_number = data.get('roll_number', ''),
            cgpa = data.get('cgpa', 0.0),
            graduation_year = data.get('graduation_year', 0),
            resume_file = data.get('resume_file', ''),
            phone   = data.get('phone', '')
        )
        db.session.add(student)
        db.session.flush()

        safe_name = secure_filename(resume_file.filename)
        filename  = f"{student.id}_{safe_name}"
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        resume_file.save(save_path)

        student.resume_filename = filename
        db.session.commit()

    return jsonify({'message': 'Registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data.get('email', '')).first()

    if not user or not check_password_hash(user.password, data.get('password', '')):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    if not user.active:
        return jsonify({'error': 'Account is deactivated. Contact admin.'}), 403
    
    token = create_token(user.id, user.role)

    response = {
        'token': token,
        'role':  user.role,
        'name':  user.name,
        'id':    user.id
    }

    if user.role == 'company':
        company = Company.query.filter_by(user_id=user.id).first()
        if company:
            response['company_id']      = company.id
            response['approval_status'] = company.approval_status

    elif user.role == 'student':
        student = Student.query.filter_by(user_id=user.id).first()
        if student:
            response['student_id'] = student.id

    return jsonify(response), 200

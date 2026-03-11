from flask import Blueprint, jsonify, request, current_app
from models import db
from models.models import Student, PlacementDrive, Application, Placement
import os
from werkzeug.utils import secure_filename
from auth import require_auth
import tasks

student_bp = Blueprint("student", __name__)

def check_eligibility(student, drive):
    if drive.min_cgpa and student.cgpa < drive.min_cgpa:
        return False
    if drive.eligible_branches:
        branches = [b.strip().lower() for b in drive.eligible_branches.split(',')]
        if student.branch and student.branch.lower() not in branches:
            return False
    return True

@student_bp.route("/drives")
@require_auth("student")
def get_drives(user):
    student = Student.query.filter_by(user_id=user.id).first()
    # Students should only see drives that are open/approved
    drives = PlacementDrive.query.filter_by(status="open").all() 

    return jsonify([
        {
            "id": d.id,
            "company": d.company.company_name,
            "title": d.job_title,
            "description": d.job_description,
            "location": d.location,
            "salary": d.package or d.salary,
            "deadline": str(d.deadline) if d.deadline else None,
            "status": d.status,
            "is_eligible": check_eligibility(student, d),
            "eligibility_reason": "You do not meet the CGPA or Branch criteria" if not check_eligibility(student, d) else ""
        }
        for d in drives
    ])

@student_bp.route("/apply/<int:drive_id>", methods=["POST"])
@require_auth("student")
def apply_drive(user, drive_id):
    student = Student.query.filter_by(user_id=user.id).first()
    drive = PlacementDrive.query.get_or_404(drive_id)

    if drive.status != "open":
        return jsonify({"error":"Drive not open"}), 400

    if not check_eligibility(student, drive):
        return jsonify({"error": "You do not meet the eligibility criteria (CGPA/Branch)"}), 400
    
    # Check if already applied
    existing = Application.query.filter_by(student_id=student.id, drive_id=drive_id).first()
    if existing:
        return jsonify({"error": "Already applied to this drive"}), 400

    app = Application(
        student_id=student.id,
        drive_id=drive_id
    )
    db.session.add(app)
    db.session.commit()

    return jsonify({"message":"Applied successfully"})

@student_bp.route("/applications")
@require_auth("student")
def my_applications(user):
    student = Student.query.filter_by(user_id=user.id).first()
    apps = Application.query.filter_by(student_id=student.id).all()
    return jsonify([
        {
            "id": a.id,
            "drive": a.drive.job_title,
            "company": a.drive.company.company_name,
            "status": a.status,
            "applied_date": a.applied_date.strftime('%Y-%m-%d')
        }
        for a in apps
    ])

@student_bp.route("/profile")
@require_auth("student")
def get_profile(user):
    student = Student.query.filter_by(user_id=user.id).first()
    return jsonify({
        "name": user.name,
        "email": user.email,
        "roll_number": student.roll_number,
        "branch": student.branch,
        "year": student.year,
        "cgpa": student.cgpa,
        "phone": student.phone,
        "skills": student.skills,
        "experience": student.experience,
        "resume": student.resume_filename
    })

@student_bp.route("/profile/update", methods=["PUT"])
@require_auth("student")
def update_profile(user):
    student = Student.query.filter_by(user_id=user.id).first()
    
    if request.form:
        student.branch = request.form.get("branch", student.branch)
        student.roll_number = request.form.get("roll_number", student.roll_number)
        student.cgpa = float(request.form.get("cgpa", student.cgpa or 0))
        student.year = int(request.form.get("year", student.year or 1))
        student.phone = request.form.get("phone", student.phone)
        student.skills = request.form.get("skills", student.skills)
        student.experience = request.form.get("experience", student.experience)
    
    if 'resume' in request.files:
        file = request.files['resume']
        if file and file.filename != '':
            filename = f"{student.id}_{secure_filename(file.filename)}"
            upload_dir = current_app.config.get('UPLOAD_FOLDER', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            file.save(os.path.join(upload_dir, filename))
            student.resume_filename = filename

    db.session.commit()
    return jsonify({"message": "Profile updated successfully"})

@student_bp.route("/history")
@require_auth("student")
def placement_history(user):
    student = Student.query.filter_by(user_id=user.id).first()
    placements = Placement.query.filter_by(student_id=student.id).all()
    return jsonify([
        {
            "id": p.id,
            "company": p.company.company_name,
            "position": p.position,
            "salary": p.salary,
            "placed_on": p.placed_on.strftime('%Y-%m-%d')
        }
        for p in placements
    ])

@student_bp.route("/export-csv", methods=["POST"])
@require_auth("student")
def export_csv(user):
    student = Student.query.filter_by(user_id=user.id).first()
    tasks.export_applications_csv.delay(student.id, user.email)
    return jsonify({"message": "Export task started. You will receive an email shortly."})
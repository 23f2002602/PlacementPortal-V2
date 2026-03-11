from flask import Blueprint, request, jsonify
from models import db
from models.models import User, Student, Company, PlacementDrive, Application, Placement
from auth import require_auth
from tasks import daily_reminders
from extensions import cache
from sqlalchemy import extract
from datetime import datetime
import json

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@require_auth("admin")
def dashboard(user):
    total_students = Student.query.count()
    total_companies = Company.query.count()
    approved_companies = Company.query.filter_by(approval_status='approved').count()
    pending_companies = Company.query.filter_by(approval_status='pending').count()
    total_drives = PlacementDrive.query.count()
    approved_drives = PlacementDrive.query.filter_by(status='approved').count()
    pending_drives = PlacementDrive.query.filter_by(status='pending').count()
    total_applications = Application.query.count()
    selected_count = Application.query.filter_by(status='selected').count()

    return jsonify({
        'total_students': total_students,
        'total_companies': total_companies,
        'approved_companies': approved_companies,
        'pending_companies': pending_companies,
        'total_drives': total_drives,
        'approved_drives': approved_drives,
        'pending_drives': pending_drives,
        'total_applications': total_applications,
        'selected_count': selected_count
    }), 200

@admin_bp.route("/stats")
@require_auth("admin")
@cache.cached(timeout=300)
def get_admin_stats(user):

    students = Student.query.count()
    companies = Company.query.count()
    drives = PlacementDrive.query.count()
    placements = Placement.query.count()

    return jsonify({
        "students": students,
        "companies": companies,
        "drives": drives,
        "placements": placements
    })

@admin_bp.route("/companies/pending")
def pending_companies():

    companies = Company.query.filter_by(approval_status="pending").all()

    return jsonify([
        {
            "id": c.id,
            "company_name": c.company_name,
            "email": c.user.email
        }
        for c in companies
    ])

@admin_bp.route("/companies", methods=["GET"])
@require_auth("admin")
def get_companies(user):

    companies = Company.query.all()

    result = []

    for c in companies:

        result.append({
            "id": c.id,
            "user_id": c.user_id,
            "company_name": c.company_name,
            "industry": c.industry,
            "location": c.location,
            "hr_contact": c.hr_contact,
            "approval_status": c.approval_status,
            "is_blacklisted": c.user.is_blacklisted if c.user else False
        })

    return jsonify(result)

@admin_bp.route("/company/<int:company_id>/approve", methods=["PUT"])
@require_auth("admin")
def approve_company(user, company_id):

    company = Company.query.get_or_404(company_id)

    company.approval_status = "approved"

    db.session.commit()

    return jsonify({"message": "Company approved"})

@admin_bp.route("/company/<int:company_id>/reject", methods=["PUT"])
@require_auth("admin")
def reject_company(user, company_id):

    company = Company.query.get_or_404(company_id)

    company.approval_status = "rejected"

    db.session.commit()

    return jsonify({"message": "Company rejected"})

@admin_bp.route("/students", methods=["GET"])
@require_auth("admin")
def get_students(user):

    students = Student.query.all()

    result = []

    for s in students:
        user = User.query.get(s.user_id)

        result.append({
            "id": s.id,
            "user_id": s.user_id,
            "name": user.name if user else "",
            "email": user.email if user else "",
            "roll_number": s.roll_number,
            "branch": s.branch,
            "cgpa": s.cgpa,
            "year": s.year,
            "is_active": user.is_active if user else True,
            "is_blacklisted": user.is_blacklisted if user else False
        })

    return jsonify(result)

@admin_bp.route("/student/<int:student_id>/delete", methods=["DELETE"])
@require_auth("admin")
def delete_student(user, student_id):
    student = Student.query.get_or_404(student_id)
    user_to_delete = User.query.get(student.user_id)
    
    db.session.delete(student)
    if user_to_delete:
        db.session.delete(user_to_delete)
        
    db.session.commit()
    return jsonify({"message": "Student deleted successfully"})

@admin_bp.route("/student/<int:student_id>/update", methods=["PUT"])
@require_auth("admin")
def admin_update_student(user, student_id):
    student = Student.query.get_or_404(student_id)
    data = request.get_json()
    
    student.branch = data.get('branch', student.branch)
    student.roll_number = data.get('roll_number', student.roll_number)
    student.cgpa = float(data.get('cgpa', student.cgpa))
    student.year = int(data.get('year', student.year))
    
    db.session.commit()
    return jsonify({"message": "Student updated successfully"})
@admin_bp.route("/search", methods=["GET"])
@require_auth("admin")
def search(user):
    q = request.args.get('q', '')
    role = request.args.get('role', 'student')
    
    if role == 'student':
        results = Student.query.join(User).filter(
            (User.name.ilike(f'%{q}%')) | (Student.roll_number.ilike(f'%{q}%'))
        ).all()
        return jsonify([{
            "id": s.id, "user_id": s.user_id, "name": s.user.name, "email": s.user.email, 
            "roll_number": s.roll_number, "branch": s.branch, "cgpa": s.cgpa,
            "is_active": s.user.is_active, "is_blacklisted": s.user.is_blacklisted
        } for s in results])
    else:
        results = Company.query.filter(Company.company_name.ilike(f'%{q}%')).all()
        return jsonify([{
            "id": c.id, "name": c.company_name, "industry": c.industry
        } for c in results])

@admin_bp.route("/drives", methods=["GET"])
@require_auth("admin")
def get_drives(user):

    drives = PlacementDrive.query.all()

    result = []

    for d in drives:
        company = Company.query.get(d.company_id)

        result.append({
            "id": d.id,
            "company": company.company_name if company else "",
            "job_title": d.job_title,
            "package": d.package,
            "deadline": str(d.deadline),
            "status": d.status
        })

    return jsonify(result)

@admin_bp.route("/drives/pending")
def pending_drives():

    drives = PlacementDrive.query.filter_by(
        status="pending_approval"
    ).all()

    return jsonify([
        {
            "id": d.id,
            "company": d.company.company_name,
            "title": d.job_title
        }
        for d in drives
    ])


@admin_bp.route("/drive/<int:drive_id>/approve", methods=["PUT"])
@require_auth("admin")
def approve_drive(user, drive_id):

    drive = PlacementDrive.query.get_or_404(drive_id)

    drive.status = "open"

    db.session.commit()

    return jsonify({"message": "Drive approved"})

@admin_bp.route("/drive/<int:drive_id>/reject", methods=["PUT"])
@require_auth("admin")
def reject_drive(user, drive_id):

    drive = PlacementDrive.query.get_or_404(drive_id)

    drive.status = "rejected"

    db.session.commit()

    return jsonify({"message": "Drive rejected"})

@admin_bp.route("/user/<int:user_id>/deactivate", methods=["PUT"])
@require_auth("admin")
def deactivate_user(user, user_id):

    user = User.query.get_or_404(user_id)

    user.is_active = False

    db.session.commit()

    return jsonify({"message": "User deactivated"})

@admin_bp.route("/user/<int:user_id>/activate", methods=["PUT"])
@require_auth("admin")
def activate_user(user, user_id):

    user = User.query.get_or_404(user_id)

    user.is_active = True

    db.session.commit()

    return jsonify({"message": "User activated"})

@admin_bp.route("/user/<int:user_id>/blacklist", methods=["PUT"])
@require_auth("admin")
def blacklist_user(user, user_id):
    user = User.query.get_or_404(user_id)
    user.is_blacklisted = not getattr(user, 'is_blacklisted', False) # Toggle blacklist
    db.session.commit()
    status = 'blacklisted' if user.is_blacklisted else 'unblacklisted'
    return jsonify({"message": f"User {status}"})


@admin_bp.route("/applications")
@require_auth("admin")
@cache.cached(timeout=300)
def get_all_applications(user):
    apps = Application.query.all()
    return jsonify([
        {
            "id": a.id,
            "student": a.student.user.name if a.student and a.student.user else "N/A",
            "company": a.drive.company.company_name if a.drive and a.drive.company else "N/A",
            "drive": a.drive.job_title if a.drive else "N/A",
            "status": a.status,
            "applied_date": a.applied_date.strftime('%Y-%m-%d')
        }
        for a in apps
    ])

@admin_bp.route("/placements", methods=["GET"])
@require_auth("admin")
def placements(user):
    placements = Placement.query.all()
    return jsonify([
        {   
            "id": p.id,
            "student": p.student.user.name if p.student and p.student.user else "",
            "company": p.company.company_name if p.company else "",
            "job_title": p.job_title,
            "package": p.package,
            "placed_on": str(p.placed_on)
        }
        for p in placements
    ])

@admin_bp.route("/application/<int:id>/delete", methods=["DELETE"])
@require_auth("admin")
def delete_application(user, id):
    app = Application.query.get_or_404(id)
    db.session.delete(app)
    db.session.commit()
    return jsonify({"message": "Application deleted"})

@admin_bp.route("/reports/monthly", methods=["GET"])
@require_auth("admin")
def monthly_report(user):
    year = int(request.args.get('year', datetime.utcnow().year))
    month = int(request.args.get('month', datetime.utcnow().month))

    # Ported monthly filter logic using extract
    drives = PlacementDrive.query.filter(
        extract('year', PlacementDrive.created_at) == year,
        extract('month', PlacementDrive.created_at) == month
    ).all()

    return jsonify({
        "year": year, "month": month,
        "drives_count": len(drives),
        "drives": [{"id": d.id, "company": d.company.company_name, "title": d.job_title} for d in drives]
    })

@admin_bp.route("/company/<int:company_id>/update", methods=["PUT"])
@require_auth("admin")
def admin_update_company(user, company_id):
    company = Company.query.get_or_404(company_id)
    data = request.get_json()
    company.company_name = data.get('company_name', company.company_name)
    company.industry = data.get('industry', company.industry)
    company.location = data.get('location', company.location)
    db.session.commit()
    return jsonify({"message": "Company updated"})

@admin_bp.route("/company/<int:company_id>/delete", methods=["DELETE"])
@require_auth("admin")
def delete_company(user, company_id):
    company = Company.query.get_or_404(company_id)
    user_to_delete = User.query.get(company.user_id)
    db.session.delete(company)
    if user_to_delete:
        db.session.delete(user_to_delete)
    db.session.commit()
    return jsonify({"message": "Company deleted"})

@admin_bp.route("/drive/<int:drive_id>/update", methods=["PUT"])
@require_auth("admin")
def admin_update_drive(user, drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    data = request.get_json()
    drive.job_title = data.get('job_title', drive.job_title)
    drive.package = data.get('package', drive.package)
    drive.status = data.get('status', drive.status)
    db.session.commit()
    return jsonify({"message": "Drive updated"})

@admin_bp.route("/drive/<int:drive_id>/delete", methods=["DELETE"])
@require_auth("admin")
def delete_drive(user, drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    db.session.delete(drive)
    db.session.commit()
    return jsonify({"message": "Drive deleted"})

@admin_bp.route("/placement/<int:id>/update", methods=["PUT"])
@require_auth("admin")
def admin_update_placement(user, id):
    p = Placement.query.get_or_404(id)
    data = request.get_json()
    p.job_title = data.get('job_title', p.job_title)
    p.salary = data.get('salary', p.salary)
    db.session.commit()
    return jsonify({"message": "Placement updated"})

@admin_bp.route("/placement/<int:id>/delete", methods=["DELETE"])
@require_auth("admin")
def delete_placement(user, id):
    p = Placement.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "Placement deleted"})
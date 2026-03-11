from flask import Blueprint, request, jsonify
from models import db
from models.models import Company, PlacementDrive, Application, Placement
from auth import require_auth
from tasks import send_application_notification
from datetime import datetime

company_bp = Blueprint("company", __name__)

from extensions import cache

@company_bp.route("/profile")
@require_auth("company")
@cache.cached(timeout=600)
def get_company_profile(user):
    company = Company.query.filter_by(user_id=user.id).first()
    if not company:
        return jsonify({"error": "Company not found"}), 404
    
    return jsonify({
        "company_name": company.company_name,
        "description": company.description,
        "industry": company.industry,
        "location": company.location,
        "hr_contact": company.hr_contact,
        "website": company.website,
        "approval_status": company.approval_status
    })

@company_bp.route("/profile/update", methods=["PUT"])
@require_auth("company")
def update_company_profile(user):
    company = Company.query.filter_by(user_id=user.id).first()
    if not company:
        return jsonify({"error": "Company not found"}), 404
    
    data = request.get_json()
    company.company_name = data.get("company_name", company.company_name)
    company.description = data.get("description", company.description)
    company.industry = data.get("industry", company.industry)
    company.location = data.get("location", company.location)
    company.hr_contact = data.get("hr_contact", company.hr_contact)
    company.website = data.get("website", company.website)
    
    db.session.commit()
    return jsonify({"message": "Profile updated successfully"})

@company_bp.route("/drive/create", methods=["POST"])
@require_auth("company")
def create_drive(user):
    company = Company.query.filter_by(user_id=user.id).first()
    if company.approval_status != 'approved':
        return jsonify({"error": "Company account not approved by admin"}), 403

    data = request.get_json()
    drive = PlacementDrive(
        company_id=company.id,
        job_title=data.get("job_title"),
        job_description=data.get("job_description"),
        skills_required=data.get("skills_required"),
        min_cgpa=float(data.get("min_cgpa", 0)),
        eligible_branches=data.get("eligible_branches"),
        eligible_years=data.get("eligible_years"),
        location=data.get("location"),
        package=float(data.get("package", 0)),
        salary=float(data.get("salary", data.get("package", 0))),
        deadline=datetime.strptime(data.get("deadline"), '%Y-%m-%d') if data.get("deadline") else None,
        status="pending_approval"
    )

    db.session.add(drive)
    db.session.commit()
    return jsonify({"message": "Drive created and awaiting admin approval"}), 201


@company_bp.route("/drives")
@require_auth("company")
@cache.cached(timeout=300)
def get_company_drives(user):
    company = Company.query.filter_by(user_id=user.id).first()
    drives = PlacementDrive.query.filter_by(company_id=company.id).all()

    return jsonify([
        {
            "id": d.id,
            "title": d.job_title,
            "status": d.status,
            "deadline": str(d.deadline) if d.deadline else None,
            "applicant_count": Application.query.filter_by(drive_id=d.id).count()
        }
        for d in drives
    ])

@company_bp.route("/drive/<int:id>")
@require_auth("company")
def get_drive_details(user, id):
    company = Company.query.filter_by(user_id=user.id).first()
    drive = PlacementDrive.query.filter_by(id=id, company_id=company.id).first_or_404()
    
    return jsonify({
        "id": drive.id,
        "job_title": drive.job_title,
        "job_description": drive.job_description,
        "skills_required": drive.skills_required,
        "min_cgpa": drive.min_cgpa,
        "eligible_branches": drive.eligible_branches,
        "eligible_years": drive.eligible_years,
        "location": drive.location,
        "package": drive.package,
        "salary": drive.salary,
        "deadline": drive.deadline.strftime('%Y-%m-%d') if drive.deadline else None,
        "status": drive.status
    })

@company_bp.route("/drive/<int:id>/update", methods=["PUT"])
@require_auth("company")
def update_drive(user, id):
    company = Company.query.filter_by(user_id=user.id).first()
    drive = PlacementDrive.query.filter_by(id=id, company_id=company.id).first_or_404()
    
    data = request.get_json()
    drive.job_title = data.get("job_title", drive.job_title)
    drive.job_description = data.get("job_description", drive.job_description)
    drive.skills_required = data.get("skills_required", drive.skills_required)
    drive.min_cgpa = float(data.get("min_cgpa", drive.min_cgpa))
    drive.eligible_branches = data.get("eligible_branches", drive.eligible_branches)
    drive.eligible_years = data.get("eligible_years", drive.eligible_years)
    drive.location = data.get("location", drive.location)
    drive.package = float(data.get("package", drive.package))
    drive.salary = float(data.get("salary", drive.salary))
    if data.get("deadline"):
        drive.deadline = datetime.strptime(data.get("deadline"), '%Y-%m-%d')
    
    # If it was rejected, editing it might re-trigger approval flow if needed, 
    # but usually status stays pending or approved unless changed by admin.
    # For now, let's keep status as is or reset to pending if admin wants re-review.
    # drive.status = "pending_approval" 
    
    db.session.commit()
    return jsonify({"message": "Drive updated successfully"})

@company_bp.route("/drive/<int:id>/delete", methods=["DELETE"])
@require_auth("company")
def delete_drive(user, id):
    company = Company.query.filter_by(user_id=user.id).first()
    drive = PlacementDrive.query.filter_by(id=id, company_id=company.id).first_or_404()
    
    db.session.delete(drive)
    db.session.commit()
    return jsonify({"message": "Drive deleted successfully"})

@company_bp.route("/drive/<int:id>/applications")
@require_auth("company")
def drive_applications(user, id):
    apps = Application.query.filter_by(drive_id=id).all()
    return jsonify([
        {
            "id": a.id,
            "student": a.student.user.name,
            "email": a.student.user.email,
            "cgpa": a.student.cgpa,
            "status": a.status
        }
        for a in apps
    ])

@company_bp.route("/application/<int:id>/accept", methods=["PUT"])
@require_auth("company")
def accept_application(user, id):
    app = Application.query.get_or_404(id)
    app.status = "selected"

    # Create placement record
    placement = Placement(
        student_id=app.student_id,
        company_id=app.drive.company_id,
        application_id=app.id,
        position=app.drive.job_title,
        salary=str(app.drive.package or app.drive.salary),
        placed_on=datetime.utcnow()
    )
    db.session.add(placement)
    db.session.commit()

    send_application_notification.delay(app.student.user.name, app.drive.company.company_name, app.drive.job_title, "selected")
    return jsonify({"message":"Student selected"})

@company_bp.route("/application/<int:id>/reject", methods=["PUT"])
@require_auth("company")
def reject_application(user, id):
    app = Application.query.get_or_404(id)
    app.status = "rejected"
    db.session.commit()
    return jsonify({"message":"Student rejected"})

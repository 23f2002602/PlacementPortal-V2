from flask import Blueprint, request, jsonify
from models import *
from auth import role_required
import json

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/stats", methods=["GET"])
@role_required("admin")
def stats():

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
@role_required("admin")
def get_companies():

    companies = Company.query.all()

    result = []

    for c in companies:

        result.append({
            "id": c.id,
            "company_name": c.company_name,
            "industry": c.industry,
            "location": c.location,
            "hr_contact": c.hr_contact,
            "approval_status": c.approval_status
        })

    return jsonify(result)

@admin_bp.route("/company/<int:company_id>/approve", methods=["PUT"])
@role_required("admin")
def approve_company(company_id):

    company = Company.query.get_or_404(company_id)

    company.approval_status = "approved"

    db.session.commit()

    return jsonify({"message": "Company approved"})

@admin_bp.route("/company/<int:company_id>/reject", methods=["PUT"])
@role_required("admin")
def reject_company(company_id):

    company = Company.query.get_or_404(company_id)

    company.approval_status = "rejected"

    db.session.commit()

    return jsonify({"message": "Company rejected"})

@admin_bp.route("/students", methods=["GET"])
@role_required("admin")
def get_students():

    students = Student.query.all()

    result = []

    for s in students:
        user = User.query.get(s.user_id)

        result.append({
            "id": s.id,
            "name": user.name if user else "",
            "email": user.email if user else "",
            "roll_number": s.roll_number,
            "branch": s.branch,
            "cgpa": s.cgpa,
            "year": s.year
        })

    return jsonify(result)

@admin_bp.route("/drives", methods=["GET"])
@role_required("admin")
def get_drives():

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
@role_required("admin")
def approve_drive(drive_id):

    drive = PlacementDrive.query.get_or_404(drive_id)

    drive.status = "open"

    db.session.commit()

    return jsonify({"message": "Drive approved"})

@admin_bp.route("/drive/<int:drive_id>/reject", methods=["PUT"])
@role_required("admin")
def reject_drive(drive_id):

    drive = PlacementDrive.query.get_or_404(drive_id)

    drive.status = "rejected"

    db.session.commit()

    return jsonify({"message": "Drive rejected"})

@admin_bp.route("/user/<int:user_id>/deactivate", methods=["PUT"])
@role_required("admin")
def deactivate_user(user_id):

    user = User.query.get_or_404(user_id)

    user.is_active = False

    db.session.commit()

    return jsonify({"message": "User deactivated"})
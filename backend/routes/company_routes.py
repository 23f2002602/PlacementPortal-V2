from flask import Blueprint, request, jsonify
from models import *
from auth import require_auth

company_bp = Blueprint("company", __name__)


@company_bp.route("/drive/create", methods=["POST"])
@require_auth("company")
def create_drive(user):

    company = Company.query.filter_by(user_id=user.id).first()

    data = request.get_json()

    drive = PlacementDrive(
        company_id=company.id,
        job_title=data.get("job_title"),
        job_description=data.get("job_description"),
        skills_required=data.get("skills_required"),
        min_cgpa=data.get("min_cgpa"),
        eligible_branches=data.get("eligible_branches"),
        eligible_years=data.get("eligible_years"),
        location=data.get("location"),
        salary=data.get("salary"),
        deadline=data.get("deadline"),
        status="pending_approval"
    )

    db.session.add(drive)
    db.session.commit()

    return jsonify({"message": "Drive created and awaiting admin approval"})


@company_bp.route("/drives")
@require_auth("company")
def get_company_drives(user):

    company = Company.query.filter_by(user_id=user.id).first()

    drives = PlacementDrive.query.filter_by(company_id=company.id).all()

    return jsonify([
        {
            "id": d.id,
            "title": d.job_title,
            "status": d.status,
            "deadline": d.deadline
        }
        for d in drives
    ])
from flask import Blueprint, jsonify
from models import PlacementDrive
from auth import require_auth

student_bp = Blueprint("student", __name__)


@student_bp.route("/drives")
@require_auth("student")
def get_drives(user):

    drives = PlacementDrive.query.all()

    return jsonify([
        {
            "id": d.id,
            "company": d.company.company_name,
            "title": d.job_title,
            "location": d.location,
            "salary": d.salary,
            "deadline": d.deadline,
            "status": d.status
        }
        for d in drives
    ])
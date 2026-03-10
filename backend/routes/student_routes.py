from flask import Blueprint, jsonify
from models import *
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

@student_bp.route("/apply/<int:drive_id>", methods=["POST"])
@require_auth("student")
def apply_drive(user, drive_id):

    student = Student.query.filter_by(user_id=user.id).first()

    drive = PlacementDrive.query.get_or_404(drive_id)

    if drive.status != "open":
        return jsonify({"error":"Drive not open"}),400

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
            "drive": a.drive.job_title,
            "company": a.drive.company.company_name,
            "status": a.status
        }
        for a in apps
    ])
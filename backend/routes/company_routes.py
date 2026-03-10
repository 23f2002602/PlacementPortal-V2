from flask import Blueprint, request, jsonify
from models import *
from auth import require_auth
from tasks import send_application_notification

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

@company_bp.route("/drive/<int:id>/applications")
@require_auth("company")
def drive_applications(user, id):

    apps = Application.query.filter_by(drive_id=id).all()

    return jsonify([
        {
            "id": a.id,
            "student": a.student.user.name,
            "email": a.student.user.email,
            "status": a.status
        }
        for a in apps
    ])



@company_bp.route("/application/<int:id>/accept", methods=["PUT"])
@require_auth("company")
def accept_application(user, id):

    app = Application.query.get_or_404(id)

    app.status = "selected"

    placement = Placement(
        student_id=app.student_id,
        company_id=app.drive.company_id,
        job_title=app.drive.job_title,
        salary=app.drive.salary,
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
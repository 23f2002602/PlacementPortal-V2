from celery_worker import celery
from models import db
from models.models import Student, User, PlacementDrive, Application, Company, Placement
from datetime import datetime, timedelta
import csv
import io
import os

@celery.task
def send_registration_email(email, name):
    print(f"Sending welcome email to {name} ({email})")
    return "email sent"

@celery.task
def send_application_notification(student, company, drive_title, status):
    print(f"Notify {student} about {drive_title} application result from {company}: {status}")
    return "notification sent"

@celery.task
def daily_reminders():
    # Remind students about upcoming deadlines (e.g., within next 24 hours)
    now = datetime.utcnow()
    tomorrow = now + timedelta(days=1)
    drives = PlacementDrive.query.filter(PlacementDrive.deadline > now, PlacementDrive.deadline <= tomorrow).all()
    
    for drive in drives:
        # Simplified: just log for now as per "print" pattern in tasks.py
        print(f"REMINDER: Drive '{drive.job_title}' for '{drive.company.company_name}' has a deadline on {drive.deadline}!")
    
    return f"Processed {len(drives)} drives for reminders"

@celery.task
def monthly_report_task():
    # Runs on 1st of every month
    now = datetime.utcnow()
    # Logic for last month
    first_of_this_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_month_end = first_of_this_month - timedelta(seconds=1)
    last_month_start = last_month_end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    drives_conducted = PlacementDrive.query.filter(PlacementDrive.created_at >= last_month_start, PlacementDrive.created_at <= last_month_end).count()
    applied_count = Application.query.filter(Application.applied_date >= last_month_start, Application.applied_date <= last_month_end).count()
    selected_count = Application.query.filter(Application.status == 'selected', Application.applied_date >= last_month_start, Application.applied_date <= last_month_end).count()

    admin = User.query.filter_by(role='admin').first()
    if admin:
        html_report = f"""
        <html>
            <body>
                <h2 style='color: #0d6efd;'>Monthly Placement Activity Report</h2>
                <p>Period: {last_month_start.strftime('%B %Y')}</p>
                <table border='1' cellpadding='10' style='border-collapse: collapse;'>
                    <tr style='background-color: #f8f9fa;'>
                        <th>Metric</th>
                        <th>Value</th>
                    </tr>
                    <tr>
                        <td>Drives Conducted</td>
                        <td>{drives_conducted}</td>
                    </tr>
                    <tr>
                        <td>Total Applications</td>
                        <td>{applied_count}</td>
                    </tr>
                    <tr>
                        <td>Total Students Selected</td>
                        <td><strong style='color: #198754;'>{selected_count}</strong></td>
                    </tr>
                </table>
                <p style='color: #6c757d; font-size: 0.9em; margin-top: 20px;'>Generated automatically by Placement Portal V2</p>
            </body>
        </html>
        """
        # In a real app, use a mailer here. For now, we simulate with print.
        print(f"EMAIL SENT TO {admin.email} WITH HTML REPORT:\n{html_report}")
    
    return "Monthly HTML report generated and sent"

@celery.task
def export_applications_csv(student_id):
    student = Student.query.get(student_id)
    if not student:
        return "Student not found"
        
    apps = Application.query.filter_by(student_id=student_id).all()
    
    # Path to save CSV in backend/uploads/exports
    export_dir = os.path.join(os.getcwd(), 'uploads', 'exports')
    os.makedirs(export_dir, exist_ok=True)
    filename = f"applications_{student_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = os.path.join(export_dir, filename)
    
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Student ID', 'Company Name', 'Drive Title', 'Application Status', 'Date'])
        for a in apps:
            writer.writerow([
                student.roll_number,
                a.drive.company.company_name,
                a.drive.job_title,
                a.status,
                a.applied_date.strftime('%Y-%m-%d')
            ])
            
    print(f"CSV exported for student {student_id}: {filepath}")
    return filepath
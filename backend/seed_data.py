import os
from app import create_app
from models import db
from models.models import User, Company, PlacementDrive, Student
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def seed_dummy_data():
    app = create_app()
    with app.app_context():
        # Create dummy companies
        companies_data = [
            {
                "name": "Google",
                "email": "hr@google.com",
                "password": "password123",
                "company_name": "Google LLC",
                "industry": "Technology",
                "location": "Mountain View, CA",
                "description": "A global leader in search and advertising."
            },
            {
                "name": "Microsoft",
                "email": "hr@microsoft.com",
                "password": "password123",
                "company_name": "Microsoft Corporation",
                "industry": "Software",
                "location": "Redmond, WA",
                "description": "Empowering every person and every organization on the planet to achieve more."
            },
            {
                "name": "TCS",
                "email": "hr@tcs.com",
                "password": "password123",
                "company_name": "Tata Consultancy Services",
                "industry": "IT Services",
                "location": "Mumbai, India",
                "description": "A global leader in IT services, consulting & business solutions."
            }
        ]

        for data in companies_data:
            if not User.query.filter_by(email=data["email"]).first():
                user = User(
                    name=data["name"],
                    email=data["email"],
                    password=generate_password_hash(data["password"]),
                    role="company"
                )
                db.session.add(user)
                db.session.flush()

                company = Company(
                    user_id=user.id,
                    company_name=data["company_name"],
                    industry=data["industry"],
                    location=data["location"],
                    description=data["description"],
                    approval_status="approved"
                )
                db.session.add(company)
                db.session.flush()

                # Add dummy drives for each company
                drive1 = PlacementDrive(
                    company_id=company.id,
                    job_title="Software Engineer",
                    job_description="Develop high-quality software solutions.",
                    skills_required="Python, JavaScript, SQL",
                    min_cgpa=7.5,
                    eligible_branches="CSE, IT",
                    eligible_years="2024, 2025",
                    location=data["location"],
                    salary=1500000,
                    package=15.0,
                    deadline=datetime.utcnow() + timedelta(days=30),
                    status="open"
                )
                drive2 = PlacementDrive(
                    company_id=company.id,
                    job_title="Data Analyst",
                    job_description="Analyze data and provide insights.",
                    skills_required="Python, R, Tableau",
                    min_cgpa=7.0,
                    eligible_branches="CSE, IT, ECE",
                    eligible_years="2024, 2025",
                    location=data["location"],
                    salary=1000000,
                    package=10.0,
                    deadline=datetime.utcnow() + timedelta(days=15),
                    status="open"
                )
                db.session.add(drive1)
                db.session.add(drive2)

        # Create a dummy student for testing
        student_email = "student@test.com"
        if not User.query.filter_by(email=student_email).first():
            user = User(
                name="Test Student",
                email=student_email,
                password=generate_password_hash("password123"),
                role="student"
            )
            db.session.add(user)
            db.session.flush()

            student = Student(
                user_id=user.id,
                roll_number="STUDENT001",
                branch="CSE",
                cgpa=8.5,
                year=3,
                phone="1234567890",
                skills="Python, Vue.js",
                experience="Intern at LocalTech"
            )
            db.session.add(student)

        db.session.commit()
        print("Dummy data seeded successfully!")

if __name__ == "__main__":
    seed_dummy_data()

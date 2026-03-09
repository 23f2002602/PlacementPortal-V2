from datetime import datetime

from . import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String)
    active = db.Column(db.Boolean, default=True)

    student = db.relationship("Student", back_populates="user", uselist=False)
    company = db.relationship("Company", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User {self.email} [{self.role}]>"
    
class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    branch = db.Column(db.String(80))
    cgpa = db.Column(db.Float, default=0.0)
    year = db.Column(db.Integer)
    phone = db.Column(db.String(20))
    skills = db.Column(db.Text)
    experience = db.Column(db.Text)
    resume_filename = db.Column(db.String(300))

    user = db.relationship("User", back_populates="student")
    applications = db.relationship("Application", back_populates="student", cascade="all, delete-orphan")
    placements = db.relationship("Placement", back_populates="student")

    def __repr__(self):
        return f"<Student {self.user.name if self.user else self.id}>"

    
class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    company_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    industry = db.Column(db.String(100))
    location = db.Column(db.String(150))
    hr_contact = db.Column(db.String(120))
    website = db.Column(db.String(200))
    approval_status = db.Column(db.String(20), default="pending")

    user = db.relationship("User", back_populates="company")
    drives = db.relationship("PlacementDrive", back_populates="company", cascade="all, delete-orphan")
    placements = db.relationship("Placement", back_populates="company")

    def __repr__(self):
        return f"<Company {self.company_name}>"

class PlacementDrive(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    job_title = db.Column(db.String(150), nullable=False)
    job_description = db.Column(db.String)
    skills_required = db.Column(db.Text)
    min_cgpa = db.Column(db.Float, default=0.0)
    eligible_branches = db.Column(db.String(300))
    eligible_years = db.Column(db.String(100))
    location = db.Column(db.String)
    salary = db.Column(db.Float)
    deadline = db.Column(db.DateTime)
    status = db.Column(db.String(30), default="open")

    company = db.relationship("Company", back_populates="drives")
    applications = db.relationship("Application", backref = "drive", lazy = True)

    def __repr__(self):
        return f'<PlacementDrive {self.job_title}>'

class Application(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey("placement_drive.id"), nullable=False)
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(30), default="applied")

    interview_date = db.Column(db.DateTime)
    interview_notes = db.Column(db.Text)
    offer_letter_file = db.Column(db.String(300))

    placement = db.relationship('Placement', back_populates='application', uselist=False, cascade='all, delete-orphan')
    student = db.relationship('Student', back_populates='applications')
    drive = db.relationship('PlacementDrive', back_populates='applications')
    
    __table_args__ = (
        db.UniqueConstraint('student_id', 'drive_id', name='uq_student_drive'),
    )

    def __repr__(self):
        return f'<Application student={self.student_id} drive={self.drive_id} status={self.status}>'


class Placement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    position = db.Column(db.String(150))
    salary = db.Column(db.String(50))             
    joining_date = db.Column(db.Date)
    placed_on = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('Student', backref='placements')
    company = db.relationship('Company', backref='placements')
    application = db.relationship('Application', back_populates='placement')

    def __repr__(self):
        return f"<Placement student={self.student_id} company={self.company_id}>"
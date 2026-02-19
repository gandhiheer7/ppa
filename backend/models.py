import os
from extensions import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    active_flag = db.Column(db.Boolean, default=True, nullable=False)
    blacklist_flag = db.Column(db.Boolean, default=False, nullable=False)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    company_profile = db.relationship('CompanyProfile', backref='user', uselist=False, cascade="all, delete-orphan")
    student_profile = db.relationship('StudentProfile', backref='user', uselist=False, cascade="all, delete-orphan")

class CompanyProfile(db.Model):
    __tablename__ = 'company_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    company_name = db.Column(db.String(150), nullable=False)
    hr_contact = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(255))
    approval_status = db.Column(db.String(20), default='Pending', nullable=False)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    drives = db.relationship('PlacementDrive', backref='company_profile', cascade="all, delete-orphan")

class StudentProfile(db.Model):
    __tablename__ = 'student_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    branch = db.Column(db.String(100), nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    passing_year = db.Column(db.Integer, nullable=False)
    resume_path = db.Column(db.String(255))
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    applications = db.relationship('Application', backref='student_profile', cascade="all, delete-orphan")

class PlacementDrive(db.Model):
    __tablename__ = 'placement_drives'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company_profiles.id'), nullable=False)
    job_title = db.Column(db.String(150), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    eligibility_branch = db.Column(db.String(100))
    eligibility_cgpa = db.Column(db.Float)
    eligibility_year = db.Column(db.Integer)
    application_deadline = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    applications = db.relationship('Application', backref='drive', cascade="all, delete-orphan")

class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drives.id'), nullable=False)
    application_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    status = db.Column(db.String(20), default='Applied', nullable=False)
    interview_date = db.Column(db.DateTime, nullable=True) # Added for scheduling
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.UniqueConstraint('student_id', 'drive_id', name='uq_student_drive_application'),
    )

def create_admin_if_not_exists():
    admin_exists = User.query.filter_by(role='Admin').first()
    if not admin_exists:
        admin_user = User(
            username='admin',
            password=generate_password_hash(os.environ.get("DEFAULT_ADMIN_PASSWORD", "change-me")),
            role='Admin',
            active_flag=True,
            blacklist_flag=False
        )
        db.session.add(admin_user)
        db.session.commit()
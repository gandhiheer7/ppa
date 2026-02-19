import os
import glob
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
from flask_jwt_extended import get_jwt_identity
from datetime import datetime, timezone
from models import db, StudentProfile, PlacementDrive, Application, CompanyProfile
from utils.decorators import student_required
from tasks import export_applications_csv
from extensions import cache

student_bp = Blueprint('student', __name__, url_prefix='/api/student')

def get_current_student():
    user_id = get_jwt_identity()
    return StudentProfile.query.filter_by(user_id=user_id).first()

@student_bp.route('/profile', methods=['PUT'])
@student_required
def update_profile():
    student = get_current_student()
    data = request.get_json()
    
    if 'branch' in data: student.branch = data['branch']
    if 'cgpa' in data: student.cgpa = float(data['cgpa'])
    if 'passing_year' in data: student.passing_year = int(data['passing_year'])
    
    db.session.commit()
    return jsonify({"msg": "Profile updated successfully"}), 200

@student_bp.route('/profile/resume', methods=['POST'])
@student_required
def upload_resume():
    student = get_current_student()
    if 'resume' not in request.files:
        return jsonify({"msg": "No resume file provided"}), 400
        
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"msg": "No selected file"}), 400
        
    filename = secure_filename(f"user_{student.user_id}_{file.filename}")
    filepath = os.path.join(current_app.config['BASE_DIR'], 'uploads', filename)
    file.save(filepath)
    
    student.resume_path = filepath
    db.session.commit()
    return jsonify({"msg": "Resume uploaded successfully"}), 200

@student_bp.route('/drives', methods=['GET'])
@student_required
@cache.cached(timeout=60, query_string=True)
def get_approved_drives():
    student = get_current_student()
    now = datetime.now(timezone.utc)
    
    # 1. Fetch ALL active approved drives
    drives = PlacementDrive.query.filter(
        PlacementDrive.status == 'Approved',
        PlacementDrive.application_deadline > now
    ).order_by(PlacementDrive.application_deadline.asc()).all()
    
    search_query = request.args.get('q', '').lower()
    
    drives_data = []
    for drive in drives:
        # 2. FILTER: Search Query
        if search_query and search_query not in drive.job_title.lower():
            continue

        # 3. FILTER: Check Eligibility (The Logic You Needed)
        # If drive has a branch requirement, student must match it
        if drive.eligibility_branch and drive.eligibility_branch.lower() != student.branch.lower():
            continue
            
        # If drive has a CGPA requirement, student must meet it
        if drive.eligibility_cgpa is not None and student.cgpa < drive.eligibility_cgpa:
            continue
        
        # Safe Company Name Fetch
        company = CompanyProfile.query.get(drive.company_id)
            
        drives_data.append({
            "drive_id": drive.id,
            "job_title": drive.job_title,
            "company_name": company.company_name if company else "Unknown",
            "eligibility_branch": drive.eligibility_branch,
            "eligibility_cgpa": drive.eligibility_cgpa,
            "application_deadline": drive.application_deadline.isoformat()
        })
        
    return jsonify({"drives": drives_data}), 200

@student_bp.route('/search/companies', methods=['GET'])
@student_required
def search_companies():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"companies": []}), 200
        
    companies = CompanyProfile.query.filter(
        CompanyProfile.company_name.ilike(f'%{query}%'), 
        CompanyProfile.approval_status == 'Approved'
    ).all()
    
    companies_data = [{"company_id": c.id, "company_name": c.company_name} for c in companies]
    return jsonify({"companies": companies_data}), 200

@student_bp.route('/drives/<int:drive_id>/apply', methods=['POST'])
@student_required
def apply_to_drive(drive_id):
    student = get_current_student()
    if not student.resume_path:
        return jsonify({"msg": "Resume upload is required before applying"}), 403

    drive = PlacementDrive.query.get(drive_id)
    if not drive or drive.status != 'Approved':
        return jsonify({"msg": "Drive not found or not approved"}), 404

    # Double-check eligibility on Apply (Security Best Practice)
    if drive.eligibility_branch and drive.eligibility_branch.lower() != student.branch.lower():
        return jsonify({"msg": "Branch eligibility not met"}), 403
    if drive.eligibility_cgpa is not None and student.cgpa < drive.eligibility_cgpa:
        return jsonify({"msg": "CGPA eligibility not met"}), 403

    if Application.query.filter_by(student_id=student.id, drive_id=drive.id).first():
        return jsonify({"msg": "You have already applied"}), 409

    new_app = Application(student_id=student.id, drive_id=drive.id)
    db.session.add(new_app)
    db.session.commit()
    return jsonify({"msg": "Applied successfully"}), 201

@student_bp.route('/applications', methods=['GET'])
@student_required
def get_student_applications():
    student = get_current_student()
    applications = Application.query.filter_by(student_id=student.id).all()
    applications_data = []
    for app in applications:
        applications_data.append({
            "application_id": app.id,
            "job_title": app.drive.job_title if app.drive else None,
            "status": app.status,
            "application_date": app.application_date.isoformat()
        })
    return jsonify({"applications": applications_data}), 200

@student_bp.route('/export-history', methods=['POST'])
@student_required
def trigger_history_export():
    student = get_current_student()
    export_applications_csv.delay(student.id, student.user.username)
    return jsonify({"msg": "Batch job triggered. Please wait a few seconds and refresh to download."}), 202

@student_bp.route('/exports', methods=['GET'])
@student_required
def get_my_exports():
    student = get_current_student()
    username = student.user.username
    upload_folder = os.path.join(current_app.config['BASE_DIR'], 'uploads')
    
    files = glob.glob(os.path.join(upload_folder, f"export_{username}_*.csv"))
    files.sort(key=os.path.getmtime, reverse=True)
    
    export_files = [os.path.basename(f) for f in files]
    return jsonify({"files": export_files}), 200
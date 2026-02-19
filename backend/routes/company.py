import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from datetime import datetime
from models import db, CompanyProfile, PlacementDrive, Application
from utils.decorators import company_required

company_bp = Blueprint('company', __name__, url_prefix='/api/company')

def get_current_company():
    user_id = get_jwt_identity()
    return CompanyProfile.query.filter_by(user_id=user_id).first()

@company_bp.route('/drives', methods=['POST'])
@company_required
def create_drive():
    company = get_current_company()
    if not company:
        return jsonify({"msg": "Company profile not found"}), 404

    if company.approval_status != 'Approved':
        return jsonify({"msg": "Company must be approved by Admin before creating drives"}), 403

    data = request.get_json()
    required_fields = ['job_title', 'job_description', 'application_deadline']
    if not all(field in data for field in required_fields):
        return jsonify({"msg": "Missing required fields"}), 400

    try:
        eligibility_cgpa_val = float(data['eligibility_cgpa']) if data.get('eligibility_cgpa') else None
        eligibility_year_val = int(data['eligibility_year']) if data.get('eligibility_year') else None
        deadline = datetime.fromisoformat(data['application_deadline'].replace("Z", "+00:00"))
        
        new_drive = PlacementDrive(
            company_id=company.id,
            job_title=data['job_title'],
            job_description=data['job_description'],
            eligibility_branch=data.get('eligibility_branch'),
            eligibility_cgpa=eligibility_cgpa_val,
            eligibility_year=eligibility_year_val,
            application_deadline=deadline,
            status='Pending'
        )
        db.session.add(new_drive)
        db.session.commit()
        return jsonify({"msg": "Placement drive created successfully. Pending Admin approval."}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Failed to create drive", "error": str(e)}), 400

@company_bp.route('/drives/<int:drive_id>', methods=['PUT', 'DELETE'])
@company_required
def modify_drive(drive_id):
    company = get_current_company()
    drive = PlacementDrive.query.get(drive_id)

    if not drive or drive.company_id != company.id:
        return jsonify({"msg": "Placement drive not found or unauthorized"}), 404

    if request.method == 'DELETE':
        if drive.status == 'Approved':
            return jsonify({"msg": "Cannot delete an approved drive"}), 403
        db.session.delete(drive)
        db.session.commit()
        return jsonify({"msg": "Placement drive deleted successfully"}), 200

    # Edit Logic
    if drive.status != 'Pending':
        return jsonify({"msg": "Only 'Pending' drives can be modified."}), 403

    data = request.get_json()
    try:
        if 'job_title' in data: drive.job_title = data['job_title']
        if 'job_description' in data: drive.job_description = data['job_description']
        if 'eligibility_branch' in data: drive.eligibility_branch = data['eligibility_branch']
        if 'eligibility_cgpa' in data: 
            drive.eligibility_cgpa = float(data['eligibility_cgpa']) if data['eligibility_cgpa'] else None
        if 'application_deadline' in data: 
            drive.application_deadline = datetime.fromisoformat(data['application_deadline'].replace("Z", "+00:00"))
        
        db.session.commit()
        return jsonify({"msg": "Placement drive updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Update failed", "error": str(e)}), 400

@company_bp.route('/drives', methods=['GET'])
@company_required
def get_company_drives():
    company = get_current_company()
    drives = PlacementDrive.query.filter_by(company_id=company.id).order_by(PlacementDrive.created_at.desc()).all()
    
    drives_data = []
    for drive in drives:
        drives_data.append({
            "drive_id": drive.id,
            "job_title": drive.job_title,
            "status": drive.status,
            "applicant_count": len(drive.applications),
            "application_deadline": drive.application_deadline.isoformat(),
            # Sending these fields for the Edit Modal
            "job_description": drive.job_description,
            "eligibility_branch": drive.eligibility_branch,
            "eligibility_cgpa": drive.eligibility_cgpa
        })
    return jsonify({"drives": drives_data}), 200

@company_bp.route('/drives/<int:drive_id>/applications', methods=['GET'])
@company_required
def get_drive_applications(drive_id):
    company = get_current_company()
    drive = PlacementDrive.query.get(drive_id)

    if not drive or drive.company_id != company.id:
        return jsonify({"msg": "Unauthorized or not found"}), 403

    applications = Application.query.filter_by(drive_id=drive.id).all()
    applications_data = []
    for app in applications:
        student = app.student_profile
        # Extract filename from the full path for the frontend link
        resume_filename = os.path.basename(student.resume_path) if student.resume_path else None
        
        applications_data.append({
            "application_id": app.id,
            "student_username": student.user.username,
            "status": app.status,
            "resume_filename": resume_filename, # Added for Resume View
            "interview_date": app.interview_date.isoformat() if app.interview_date else None
        })
    return jsonify({"applications": applications_data}), 200

@company_bp.route('/applications/<int:application_id>/shortlist', methods=['POST'])
@company_required
def shortlist_application(application_id):
    company = get_current_company()
    application = Application.query.get(application_id)
    
    if not application or application.drive.company_id != company.id:
        return jsonify({"msg": "Application not found or unauthorized"}), 404

    if application.status != 'Applied':
        return jsonify({"msg": f"Cannot shortlist. Current status is '{application.status}'"}), 400

    application.status = 'Shortlisted'
    db.session.commit()
    return jsonify({"msg": "Application shortlisted successfully"}), 200

@company_bp.route('/applications/<int:application_id>/status', methods=['PUT'])
@company_required
def update_application_status(application_id):
    company = get_current_company()
    application = Application.query.get(application_id)
    
    if not application or application.drive.company_id != company.id:
        return jsonify({"msg": "Application not found or unauthorized"}), 404

    data = request.get_json()
    status = data.get('status')
    
    if status in ['Selected', 'Rejected']:
        application.status = status
    if 'interview_date' in data and data['interview_date']:
        application.interview_date = datetime.fromisoformat(data['interview_date'].replace("Z", "+00:00"))
        
    db.session.commit()
    return jsonify({"msg": f"Application status updated to {status}"}), 200

@company_bp.route('/applications/<int:application_id>/offer-letter', methods=['GET'])
@company_required
def generate_offer_letter(application_id):
    company = get_current_company()
    application = Application.query.get(application_id)
    
    if not application or application.drive.company_id != company.id:
        return jsonify({"msg": "Application not found or unauthorized"}), 404

    if application.status != 'Selected':
        return jsonify({"msg": "Offer letters can only be generated for Selected students"}), 403

    student = application.student_profile
    offer_letter_text = (
        f"OFFER LETTER\n"
        f"Company: {company.company_name}\n"
        f"Student: {student.user.username}\n"
        f"Role: {application.drive.job_title}\n"
        f"Date: {datetime.now().strftime('%Y-%m-%d')}\n\n"
        f"Dear {student.user.username},\n\n"
        f"We are pleased to offer you the position of {application.drive.job_title} at {company.company_name}.\n"
        f"We were impressed with your skills and believe you will be a valuable asset to our team.\n\n"
        f"Sincerely,\nHR Department, {company.company_name}"
    )
    return jsonify({"offer_letter": offer_letter_text}), 200
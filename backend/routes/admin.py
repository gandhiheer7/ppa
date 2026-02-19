from flask import Blueprint, request, jsonify
from models import db, User, CompanyProfile, StudentProfile, PlacementDrive, Application
from utils.decorators import admin_required
from extensions import cache

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def get_dashboard_stats():
    # We remove cache briefly to ensure you see live updates during testing
    total_students = StudentProfile.query.count()
    total_companies = CompanyProfile.query.count()
    total_drives = PlacementDrive.query.count()
    
    return jsonify({
        "total_students": total_students,
        "total_companies": total_companies,
        "total_placement_drives": total_drives
    }), 200

@admin_bp.route('/companies/<int:company_id>/approve', methods=['POST'])
@admin_required
def approve_company(company_id):
    company = CompanyProfile.query.get_or_404(company_id)
    company.approval_status = 'Approved'
    db.session.commit()
    return jsonify({"msg": "Company approved successfully"}), 200

@admin_bp.route('/companies/<int:company_id>/reject', methods=['POST'])
@admin_required
def reject_company(company_id):
    company = CompanyProfile.query.get_or_404(company_id)
    company.approval_status = 'Rejected'
    db.session.commit()
    return jsonify({"msg": "Company rejected successfully"}), 200

@admin_bp.route('/drives/<int:drive_id>/approve', methods=['POST'])
@admin_required
def approve_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = 'Approved'
    db.session.commit()
    return jsonify({"msg": "Placement drive approved successfully"}), 200

@admin_bp.route('/drives/<int:drive_id>/reject', methods=['POST'])
@admin_required
def reject_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = 'Closed'
    db.session.commit()
    return jsonify({"msg": "Placement drive rejected successfully"}), 200

@admin_bp.route('/search/students', methods=['GET'])
@admin_required
def search_students():
    query = request.args.get('q', '')
    
    if query:
        students = StudentProfile.query.join(User).filter(User.username.ilike(f'%{query}%')).all()
    else:
        students = StudentProfile.query.all()
    
    students_data = []
    for s in students:
        user = User.query.get(s.user_id)
        students_data.append({
            "student_id": s.id,
            "user_id": s.user_id,
            "username": user.username if user else "Unknown",
            "branch": s.branch,
            "cgpa": s.cgpa,
            "active": user.active_flag if user else False,
            "blacklisted": user.blacklist_flag if user else False
        })
        
    return jsonify({"students": students_data}), 200

@admin_bp.route('/search/companies', methods=['GET'])
@admin_required
def search_companies():
    query = request.args.get('q', '')
    
    if query:
        companies = CompanyProfile.query.filter(CompanyProfile.company_name.ilike(f'%{query}%')).all()
    else:
        companies = CompanyProfile.query.all()
    
    companies_data = []
    for c in companies:
        user = User.query.get(c.user_id)
        companies_data.append({
            "id": c.id,          
            "company_id": c.id,
            "user_id": c.user_id,
            "company_name": c.company_name,
            "hr_contact": c.hr_contact,       
            "approval_status": c.approval_status, 
            "status": c.approval_status,      
            "active": user.active_flag if user else False,
            "blacklisted": user.blacklist_flag if user else False
        })
        
    return jsonify({"companies": companies_data}), 200

@admin_bp.route('/search/drives', methods=['GET'])
@admin_required
def search_drives():
    query = request.args.get('q', '')
    
    if query:
        drives = PlacementDrive.query.filter(PlacementDrive.job_title.ilike(f'%{query}%')).all()
    else:
        drives = PlacementDrive.query.all()
        
    drives_data = []
    for d in drives:
        # FIX: Manually fetch company using company_id to avoid crashing if relationship is missing
        company = CompanyProfile.query.get(d.company_id)
        
        drives_data.append({
            "drive_id": d.id,
            "job_title": d.job_title,
            "company_name": company.company_name if company else "Unknown",
            "status": d.status
        })
    
    return jsonify({"drives": drives_data}), 200

@admin_bp.route('/users/<int:user_id>/blacklist', methods=['POST'])
@admin_required
def blacklist_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'Admin':
        return jsonify({"msg": "Cannot blacklist an Admin"}), 403
        
    user.active_flag = False
    user.blacklist_flag = True
    db.session.commit()
    return jsonify({"msg": f"{user.role} blacklisted successfully"}), 200

@admin_bp.route('/users/<int:user_id>/reactivate', methods=['POST'])
@admin_required
def reactivate_user(user_id):
    user = User.query.get_or_404(user_id)
    user.active_flag = True
    user.blacklist_flag = False
    db.session.commit()
    return jsonify({"msg": f"{user.role} reactivated successfully"}), 200
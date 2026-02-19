from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models import db, User, StudentProfile, CompanyProfile

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid credentials"}), 401

    if not user.active_flag:
        return jsonify({"msg": "Account is deactivated"}), 403

    if user.blacklist_flag:
        return jsonify({"msg": "Account is blacklisted"}), 403

    access_token = create_access_token(
        identity=str(user.id), 
        additional_claims={'role': user.role}
    )

    return jsonify({"access_token": access_token, "role": user.role}), 200


@auth_bp.route('/register/student', methods=['POST'])
def register_student():
    data = request.get_json()
    
    required_fields = ['username', 'password', 'branch', 'cgpa', 'passing_year']
    if not all(field in data for field in required_fields):
        return jsonify({"msg": "Missing required fields"}), 400

    try:
        cgpa_val = float(data['cgpa'])
        passing_year_val = int(data['passing_year'])
    except (ValueError, TypeError):
        return jsonify({"msg": "Invalid data format: cgpa must be a float and passing_year must be an integer"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "Username already exists"}), 409

    try:
        new_user = User(
            username=data['username'],
            password=generate_password_hash(data['password']),
            role='Student'
        )
        db.session.add(new_user)
        db.session.flush() 

        new_student_profile = StudentProfile(
            user_id=new_user.id,
            branch=data['branch'],
            cgpa=cgpa_val,
            passing_year=passing_year_val
        )
        db.session.add(new_student_profile)
        db.session.commit()

        return jsonify({"msg": "Student registered successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Registration failed", "error": str(e)}), 500


@auth_bp.route('/register/company', methods=['POST'])
def register_company():
    data = request.get_json()
    
    required_fields = ['username', 'password', 'company_name', 'hr_contact']
    if not all(field in data for field in required_fields):
        return jsonify({"msg": "Missing required fields"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "Username already exists"}), 409

    try:
        new_user = User(
            username=data['username'],
            password=generate_password_hash(data['password']),
            role='Company'
        )
        db.session.add(new_user)
        db.session.flush()

        new_company_profile = CompanyProfile(
            user_id=new_user.id,
            company_name=data['company_name'],
            hr_contact=data['hr_contact'],
            website=data.get('website', '') 
        )
        db.session.add(new_company_profile)
        db.session.commit()

        return jsonify({"msg": "Company registered successfully. Pending Admin approval."}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Registration failed", "error": str(e)}), 500
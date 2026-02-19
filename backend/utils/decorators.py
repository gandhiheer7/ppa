from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from models import User

def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            claims = get_jwt()
            
            user = User.query.get(user_id)
            if not user:
                return jsonify({"msg": "User not found"}), 404
                
            if not user.active_flag:
                return jsonify({"msg": "Account deactivated"}), 403
                
            if user.blacklist_flag:
                return jsonify({"msg": "Account blacklisted"}), 403
                
            # Verify claim role matches database role and the required role for the route
            if claims.get('role') != user.role or user.role != required_role:
                return jsonify({"msg": f"Access restricted to {required_role} role or role mismatch"}), 403
                
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def admin_required(fn):
    return role_required('Admin')(fn)

def company_required(fn):
    return role_required('Company')(fn)

def student_required(fn):
    return role_required('Student')(fn)
"""
Authentication Routes
Handles user login, registration, and token management
"""

from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import jwt
from functools import wraps
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Mock database - In production, use actual database
USERS_DB = {
    'user@vendorbridge.com': {
        'id': '1',
        'name': 'Test User',
        'email': 'user@vendorbridge.com',
        'password': generate_password_hash('password123'),
        'role': 'admin',
        'created_at': datetime.utcnow()
    },
    'vendor@example.com': {
        'id': '2',
        'name': 'Vendor User',
        'email': 'vendor@example.com',
        'password': generate_password_hash('vendor123'),
        'role': 'vendor',
        'created_at': datetime.utcnow()
    }
}

SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')


def generate_token(user_id, email, role):
    """Generate JWT token"""
    payload = {
        'user_id': user_id,
        'email': email,
        'role': role,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def token_required(f):
    """Decorator to verify JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            # Extract token from "Bearer <token>"
            token = token.split(' ')[1] if ' ' in token else token
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = data
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login endpoint
    Expected JSON: {
        "email": "user@example.com",
        "password": "password123"
    }
    """
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password are required'}), 400

    email = data.get('email').lower()
    password = data.get('password')

    # Find user in database
    user = USERS_DB.get(email)

    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid email or password'}), 401

    # Generate token
    token = generate_token(user['id'], user['email'], user['role'])

    response = {
        'token': token,
        'user': {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'role': user['role']
        },
        'message': 'Login successful'
    }

    return jsonify(response), 200


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registration endpoint
    Expected JSON: {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123",
        "role": "vendor"
    }
    """
    data = request.get_json()

    required_fields = ['name', 'email', 'password', 'role']
    if not all(data.get(field) for field in required_fields):
        return jsonify({'message': 'All fields are required'}), 400

    email = data.get('email').lower()

    # Check if user already exists
    if email in USERS_DB:
        return jsonify({'message': 'Email already registered'}), 409

    # Validate role
    if data.get('role') not in ['vendor', 'buyer', 'admin']:
        return jsonify({'message': 'Invalid role'}), 400

    # Create new user
    new_user = {
        'id': str(len(USERS_DB) + 1),
        'name': data.get('name'),
        'email': email,
        'password': generate_password_hash(data.get('password')),
        'role': data.get('role'),
        'created_at': datetime.utcnow()
    }

    USERS_DB[email] = new_user

    # Generate token
    token = generate_token(new_user['id'], new_user['email'], new_user['role'])

    response = {
        'token': token,
        'user': {
            'id': new_user['id'],
            'name': new_user['name'],
            'email': new_user['email'],
            'role': new_user['role']
        },
        'message': 'Registration successful'
    }

    return jsonify(response), 201


@auth_bp.route('/verify-token', methods=['POST'])
@token_required
def verify_token(current_user):
    """
    Verify if token is valid
    """
    return jsonify({
        'valid': True,
        'user': current_user,
        'message': 'Token is valid'
    }), 200


@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """
    Logout endpoint
    In production, implement token blacklisting
    """
    return jsonify({'message': 'Logout successful'}), 200


@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """
    Get current user profile
    """
    user = USERS_DB.get(current_user.get('email'))

    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({
        'user': {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'role': user['role'],
            'created_at': user['created_at'].isoformat()
        }
    }), 200

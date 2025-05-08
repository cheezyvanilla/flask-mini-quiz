# api.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db
from app.models import User

# Create a Blueprint for the API
api = Blueprint('api', __name__)

# API route to handle the registration
@api.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    print(data)
    
    # Validate input
    username = data.get('username')
    nickname = data.get('nickname')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if not username or not nickname or not password or not confirm_password:
        return jsonify({'error': 'All fields are required'}), 400

    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    # Check if username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already taken'}), 400

    # Create new user and hash password
    hashed_password = generate_password_hash(password, method='scrypt')
    new_user = User(username=username, nickname=nickname, password=hashed_password)

    # Add user to the database
    db.session.add(new_user)
    db.session.commit()

    # Return a response with custom serialization
    return jsonify({'message': 'User registered successfully!', 'user': new_user.serialize()})

@api.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid username or password'}), 401

    return jsonify({'message': 'Login successful', 'user': user.serialize()}), 200
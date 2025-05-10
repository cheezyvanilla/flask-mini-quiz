# api.py
from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from apps.db import db
from apps.models import User
from apps.utils.mistral_quiz import mistral_quiz
from dotenv import load_dotenv
import os
import requests
# Create a Blueprint for the API
api = Blueprint('api', __name__)

# API route to handle the registration
@api.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
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

    session['session'] = {
        'user_id': user.id,
        'username': user.username,
        'nickname': user.nickname
    }
    return jsonify({'message': 'Login successful', 'user': user.serialize()}), 200

@api.route('/api/logout', methods=['POST'])
def logout():
    session.pop('session', None)
    return jsonify({'message': 'Logout successful'})

@api.route('/api/quiz', methods=['GET'])
def get_quiz():
    prev_question = request.args.get('prev_question', 'Apa itu AI dalam konteks pemrograman Python? and Apa yang dimaksud dengan AI (Artificial Intelligence)?')
    resp = mistral_quiz(prev_question)
    return jsonify(resp)

@api.route('/api/score', methods=['POST'])
def update_score():
    # get session data
    session_data = session.get('session')
    if not session_data:
        return jsonify({'error': 'User not logged in'}), 401

    data = request.get_json()
    score = data.get('score')
    if not score:
        return jsonify({'error': 'Score is required'}), 400

    user = User.query.filter_by(username=session_data['username']).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Update and save score
    user.score = user.score + 10
    db.session.commit()
    return jsonify({'message': 'Score updated successfully'})

@api.route('/api/weather', methods=['GET'])
def get_weather():
    # Get city from query parameter
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400

    load_dotenv()
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        return jsonify({'error': 'API key not found'}), 500

    # Get coordinates for the city
    geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    geocode_response = requests.get(geocode_url)
    if geocode_response.status_code != 200 or not geocode_response.json():
        return jsonify({'error': 'City not found'}), 404

    location = geocode_response.json()[0]
    lat, lon = location['lat'], location['lon']

    # Get weather forecast
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=id"
    forecast_response = requests.get(forecast_url)
    if forecast_response.status_code != 200:
        return jsonify({'error': 'Failed to fetch weather data'}), 500

    data = forecast_response.json()
    forecast_list = data['list']

    # Process forecast data to get daily summaries
    from collections import defaultdict
    from datetime import datetime

    daily_forecast = defaultdict(list)
    for entry in forecast_list:
        date = datetime.fromtimestamp(entry['dt']).date()
        daily_forecast[date].append(entry)


    forecast_data = []
    for date, entries in list(daily_forecast.items())[:3]:
        day_weather = entries[2]['weather'][0]['description'] if len(entries) > 2 else entries[0]['weather'][0]['description']
        night_weather = entries[-1]['weather'][0]['description']

        date_str = date.strftime('%d %B %Y')
        parts = date_str.split()
        day = parts[0]
        month = month_map.get(parts[1], parts[1])  # Translate if possible
        year = parts[2]

        date_indo = f"{day} {month} {year}"
        forecast_data.append({
            'day': date.strftime('%A'),
            'date': date_indo,
            'day_weather': day_weather,
            'night_weather': night_weather
        })
    print('cekres', forecast_data)
    return jsonify({'forecast': forecast_data})

month_map = {
    'January': 'Januari',
    'February': 'Februari',
    'March': 'Maret',
    'April': 'April',
    'May': 'Mei',
    'June': 'Juni',
    'July': 'Juli',
    'August': 'Agustus',
    'September': 'September',
    'October': 'Oktober',
    'November': 'November',
    'December': 'Desember'
}
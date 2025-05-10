from flask import Flask, request, jsonify, render_template, session
from apps.db import db
from apps.api import api
from apps.models import User
# Initialize the Flask app and database
app = Flask(__name__)

# Load configuration
app.config.from_object('apps.config.Config')

# Initialize database with app
db.init_app(app)

# Register the Blueprint (API routes)
app.register_blueprint(api)  # Register the API blueprint
# Route to render the register page
@app.route('/register')
def register():
    is_logged_in = True if session.get('session') else False
    return render_template('register.html', is_logged_in=is_logged_in)

@app.route('/login')
def login():
    is_logged_in = True if session.get('session') else False
    return render_template('login.html', is_logged_in=is_logged_in)

@app.route('/')
def index():
    is_logged_in = True if session.get('session') else False
    return render_template('index.html', is_logged_in=is_logged_in)

@app.route('/quiz')
def quiz():
    # cek auth
    session_data = session.get('session')
    print(session_data)
    if not session_data:
        return render_template('login.html')
    # get user data from db
    user = User.query.filter_by(id=session_data['user_id']).first()
    print(user.__dict__)
    is_logged_in = True if session.get('session') else False
    return render_template('quiz.html', is_logged_in=is_logged_in, score=user.score)
# Create the database and tables (only needed once)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

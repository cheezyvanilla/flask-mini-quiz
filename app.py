from flask import Flask, request, jsonify, render_template
from app.db import db
from app.api import api
# Initialize the Flask app and database
app = Flask(__name__)

# Load configuration
app.config.from_object('app.config.Config')

# Initialize database with app
db.init_app(app)

# Register the Blueprint (API routes)
app.register_blueprint(api)  # Register the API blueprint
# Route to render the register page
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')
# Create the database and tables (only needed once)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

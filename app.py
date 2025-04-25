# ===============================
# app.py
# ===============================
# Main Flask app, imports and registers all routes using Blueprints

from flask import Flask
from routes.auth_routes import auth_bp
from routes.teacher_routes import teacher_bp
from routes.student_routes import student_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Register route Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(teacher_bp)
app.register_blueprint(student_bp)

if __name__ == '__main__':
    app.run(debug=True)

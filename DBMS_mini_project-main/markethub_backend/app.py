# Import necessary modules and packages
from flask import Flask, redirect, url_for, jsonify  # Flask core functionalities
from flask_cors import CORS  # For handling Cross-Origin Resource Sharing (CORS)
from routes.auth_routes import auth_bp  # Authentication related routes blueprint
from routes.auth_routes import profile_bp  # User profile related routes blueprint
from routes.supplier_routes import supplier_bp  # Supplier management routes blueprint
from datetime import datetime  # For date/time operations (currently unused in this file)
from flask import send_from_directory  # For serving static files (currently unused in this file)

# Initialize the Flask application
app = Flask(__name__)
# Set a secret key for session management and security features
# Note: In production, this should be stored in environment variables
app.secret_key = "Shanu@04082005"

# Configure Cross-Origin Resource Sharing (CORS)
# This allows the API to be accessed from different domains during development
# For production, you should restrict this to specific domains
CORS(app)  # Enables CORS for all routes with default options

# Register application blueprints (modular components)
# Blueprints help organize the application into distinct components
app.register_blueprint(auth_bp)     # Register authentication routes
app.register_blueprint(profile_bp)   # Register user profile routes
app.register_blueprint(supplier_bp)  # Register supplier management routes

# Main entry point for the application
if __name__ == '__main__':
    # Run the Flask development server
    # debug=True enables:
    # - Automatic reloader for code changes
    # - Detailed error pages
    # Note: debug should be False in production
    app.run(debug=True)

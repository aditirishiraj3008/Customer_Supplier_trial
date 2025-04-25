from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import random
import os
from flask_cors import CORS
from routes.product_routes import product_blueprint
from routes.auth_routes import auth_bp
from routes.auth_routes import profile_bp
from routes.supplier_routes import supplier_bp
from datetime import datetime
from werkzeug.utils import secure_filename

from flask import send_from_directory


app = Flask(__name__)

app.secret_key = "Shanu@04082005"

# Enable CORS
# Apply CORS to all routes
# In app.py - REPLACE your current CORS setup with this:
# In app.py - Replace your current CORS setup with this:
CORS(app)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(product_blueprint, url_prefix='/')
app.register_blueprint(supplier_bp)

if __name__ == '__main__':
    app.run(debug=True)

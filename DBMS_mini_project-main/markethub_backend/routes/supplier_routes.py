# Import required modules
from flask import Blueprint, jsonify, request, render_template  # Flask components for routing and responses
import mysql.connector  # MySQL database connector
from db import get_db_connection  # Custom database connection utility

# Create a Blueprint for supplier-related routes
# Blueprints help organize related routes and can be registered with the main Flask app
supplier_bp = Blueprint('supplier', __name__)

@supplier_bp.route('/suppliers', methods=['GET'])
def get_suppliers():
    """
    Endpoint: GET /suppliers
    Flow: 
    1. Client (frontend) makes GET request to this endpoint
    2. Server attempts to fetch all supplier data from database
    3. Returns formatted supplier data or error response
    
    Data Flow:
    Frontend → Flask Route → Database → Format Response → Frontend
    
    Returns:
    - Success: JSON with all supplier details including addresses
    - Error: JSON with error message and 500 status code
    """
    try:
        # STEP 1: Establish database connection
        # Uses the get_db_connection() utility from db.py
        conn = get_db_connection()
        
        # Create a dictionary cursor to get results as dictionaries (for easier JSON conversion)
        cursor = conn.cursor(dictionary=True)
        
        # STEP 2: Execute SQL query to fetch supplier data
        # This query:
        # - Gets basic supplier info from Supplier table
        # - Joins with Address table to get formatted address string
        # - Uses LEFT JOIN so suppliers without addresses are still included
        cursor.execute("""
            SELECT 
                s.userID, 
                s.sName as name, 
                s.email, 
                s.phoneNo as phone, 
                CONCAT(
                    a.houseNo, ', ', 
                    a.streetName, ', ', 
                    a.city, ', ', 
                    a.state, ' - ', 
                    a.pin
                ) as address
            FROM Supplier s
            LEFT JOIN Address a ON s.userID = a.userID
        """)
        
        # STEP 3: Fetch all results
        # fetchall() returns a list of dictionaries where each dict represents a supplier
        suppliers = cursor.fetchall()
        
        # STEP 4: Clean up database resources
        cursor.close()
        conn.close()
        
        # STEP 5: Return successful response
        # jsonify converts Python dict to proper JSON response
        return jsonify({
            "status": "success",
            "suppliers": suppliers  # List of all suppliers with their details
        })
        
    except Exception as e:
        # ERROR HANDLING:
        # If any error occurs in the try block (database connection, query execution, etc)
        # This block will return a 500 Internal Server Error with the error message
        return jsonify({
            "status": "error",
            "message": str(e)  # Convert exception to string for JSON serialization
        }), 500  # HTTP 500 status code for server errors

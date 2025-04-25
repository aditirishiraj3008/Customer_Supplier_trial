# Import required modules
from flask import Blueprint, jsonify, request, redirect, render_template  # Flask components for routing and responses
import mysql.connector  # MySQL database connector

# Create Blueprint instances for different route groups
auth_bp = Blueprint('auth', __name__)  # Authentication related routes
profile_bp = Blueprint('profile', __name__)  # User profile related routes

# Import database connection utility
from db import get_db_connection  # Custom module to handle database connections

# Utility function to generate new user IDs based on user type
def generate_user_id(user_type):
    """
    Generates a new user ID based on user type (Customer/Supplier)
    Format: C{number} for Customers, S{number} for Suppliers
    """
    conn = get_db_connection()  # Establish database connection
    cursor = conn.cursor()  # Create database cursor
    
    if user_type == 'Customer':
        # Get current customer count and increment
        cursor.execute("SELECT COUNT(*) FROM Customer")
        count = cursor.fetchone()[0] + 1
        user_id = f"C{count:03d}"  # Format with leading zeros (e.g., C001)
    else:
        # Get current supplier count and increment
        cursor.execute("SELECT COUNT(*) FROM Supplier")
        count = cursor.fetchone()[0] + 1
        user_id = f"S{count:03d}"  # Format with leading zeros (e.g., S001)

    # Clean up database resources
    cursor.close()
    conn.close()
    return user_id

# User registration endpoint
@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    Handles new user registration
    Accepts JSON payload with user details
    Creates records in both User and role-specific tables
    """
    data = request.json  # Get JSON data from request
    role = data.get('role')  # "Supplier" or "Customer"
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    # Validate required fields
    if not all([role, name, email, phone, password]):
        return jsonify({"status": "fail", "message": "Missing required fields"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Generate new user ID with proper formatting
        user_id = generate_user_id(role)

        # Insert into User table (credentials storage)
        cursor.execute("INSERT INTO User (userID, password) VALUES (%s, %s)", 
                      (user_id, password))

        # Insert into role-specific table
        if role == "Customer":
            cursor.execute("""
                INSERT INTO Customer (userID, cName, email, phoneNo) 
                VALUES (%s, %s, %s, %s)
            """, (user_id, name, email, phone))
        else:
            cursor.execute("""
                INSERT INTO Supplier (userID, sName, email, phoneNo) 
                VALUES (%s, %s, %s, %s)
            """, (user_id, name, email, phone))

        conn.commit()  # Commit transaction
        return {"status": "success", "userID": user_id}

    except mysql.connector.Error as err:
        conn.rollback()  # Rollback on error
        return {"status": "fail", "message": str(err)}, 500
    finally:
        # Ensure resources are always released
        cursor.close()
        conn.close()

# User authentication endpoint
@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Handles user login
    Verifies credentials against database
    Returns user role and ID if successful
    """
    data = request.get_json()  # Get JSON data from request
    email = data.get('email')
    password = data.get('password')

    # Basic input validation
    if not email or not password:
        return {"status": "fail", "message": "Email and password required"}, 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check Supplier credentials first
        cursor.execute("""
            SELECT User.userID FROM Supplier
            JOIN User ON Supplier.userID = User.userID
            WHERE Supplier.email = %s AND User.password = %s
        """, (email, password))
        supplier_result = cursor.fetchone()

        if supplier_result:
            user_id = supplier_result[0]
            role = 'Supplier'  # More descriptive than 'S'
        else:
            # Check Customer credentials if not a supplier
            cursor.execute("""
                SELECT User.userID FROM Customer
                JOIN User ON Customer.userID = User.userID
                WHERE Customer.email = %s AND User.password = %s
            """, (email, password))
            customer_result = cursor.fetchone()

            if customer_result:
                user_id = customer_result[0]
                role = 'Customer'  # More descriptive than 'C'
            else:
                return {"status": "fail", "message": "Invalid credentials"}, 401

        # Store logged-in user ID (consider using session instead)
        with open('logged_in_user.txt', 'w') as f:
            f.write(user_id)

        return {
            "status": "success", 
            "role": role,
            "userID": user_id  # Return user ID to client
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}, 500
    finally:
        cursor.close()
        conn.close()

# User profile endpoint
@profile_bp.route('/profile', methods=['GET'])
def get_profile():
    """
    Retrieves complete profile information for logged-in user
    Combines data from user table and address table
    """
    try:
        # Read current user ID from file (consider using session)
        with open("logged_in_user.txt", "r") as file:
            user_id = file.read().strip()

        if not user_id:
            return jsonify({"error": "Not logged in"}), 401

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Return results as dictionaries

        # Determine user role from ID prefix
        role = "Supplier" if user_id.startswith("S") else "Customer"

        # Fetch basic user information
        if role == "Supplier":
            cursor.execute("""
                SELECT sName AS name, email, phoneNo AS phone 
                FROM Supplier WHERE userID = %s
            """, (user_id,))
        else:
            cursor.execute("""
                SELECT cName AS name, email, phoneNo AS phone 
                FROM Customer WHERE userID = %s
            """, (user_id,))
        user_data = cursor.fetchone()

        if not user_data:
            return jsonify({"error": "User not found"}), 404

        # Fetch formatted address string
        cursor.execute("""
            SELECT CONCAT(houseNo, ', ', streetName, ', ', city, ', ', state, ' - ', pin) AS address
            FROM Address WHERE userID = %s
        """, (user_id,))
        address_data = cursor.fetchone()

        return jsonify({
            "role": role,
            "userID": user_id,
            "name": user_data["name"],
            "email": user_data["email"],
            "phone": user_data["phone"],
            "address": address_data["address"] if address_data else "Not available"
        })

    except FileNotFoundError:
        return jsonify({"error": "Not logged in"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

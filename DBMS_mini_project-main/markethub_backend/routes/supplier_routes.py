from flask import Blueprint, jsonify, request, render_template
import mysql.connector
from db import get_db_connection

supplier_bp = Blueprint('supplier', __name__)

@supplier_bp.route('/suppliers', methods=['GET'])
def get_suppliers():
    try:
        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Fetch all supplier details
        cursor.execute("""
            SELECT s.userID, s.sName as name, s.email, s.phoneNo as phone, 
                   CONCAT(a.houseNo, ', ', a.streetName, ', ', a.city, ', ', a.state, ' - ', a.pin) as address
            FROM Supplier s
            LEFT JOIN Address a ON s.userID = a.userID
        """)
        
        suppliers = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "status": "success",
            "suppliers": suppliers
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
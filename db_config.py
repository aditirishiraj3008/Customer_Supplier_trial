# Folder structure reminder:
# school_portal/
# ├── app.py
# ├── db_config.py
# ├── routes/
# │   ├── auth_routes.py
# │   ├── teacher_routes.py
# │   └── student_routes.py

# ===============================
# db_config.py
# ===============================
# This file handles the MySQL connection setup

import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="Shanu",
        password="Shanu@123",
        database="school_db"
    )

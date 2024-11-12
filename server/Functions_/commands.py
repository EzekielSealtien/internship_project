from datetime import date
import os
from pydantic import BaseModel
from typing import List, Optional
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor

# Load environment variables
DB_NAME = os.getenv("DB_NAME", "intershipDB")
DB_USER = os.getenv("DB_USER", "postgres")

DB_PORT = os.getenv("DB_PORT", "5432")

def create_connection():
    """
    Establishes a connection to the PostgreSQL database.
    """
    try:
        con = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Database connection established.")
        return con
    except OperationalError as e:
        print(f"Error connecting to the database: {e}")
        return None

# Create the connection
conn = create_connection()

# Ensure the connection is valid
if not conn:
    raise Exception("Database connection could not be established. Please check your environment variables.")

# Define Pydantic models
class Users(BaseModel):
    name: str
    email: str
    password_hash: str
    date_of_birth: str
    phone_number: str

class UserResponse(Users):
    user_id: int

class Doctor(BaseModel):
    name: str
    email: str
    password_hash: str
    specialization: Optional[str] = None
    phone_number: str

class DoctorResponse(Doctor):
    doctor_id: int

class Alerts(BaseModel):
    alert_type: str
    message: str
    status: str
    user_id: int

class AlertsResponse(Alerts):
    alert_id: int

class Health_data(BaseModel):
    heart_rate: int
    blood_pressure: int
    oxygen_level: int
    temperature: int
    user_id:int

class Health_dataRespons(Health_data):
    data_id: int

class recommendation(BaseModel):
    message: str
    alert_id: int
    user_id: int

class recommendationResponse(recommendation):
    id_recommendation: int

class UserFullInfo(BaseModel):
    user_id: int
    name: str
    email: str
    password_hash:str
    phone_number: str
    date_of_birth: Optional[date] = None
    doctor_id: Optional[int] = None
    health_data: Optional[Health_data] = None
    alerts: Optional[List[Alerts]] = []

# User management functions
def create_user(user: Users):
    if not conn:
        raise Exception("No database connection available.")
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(
            """
            INSERT INTO users (name, email, password_hash, date_of_birth, phone_number)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING user_id, name, email, password_hash, date_of_birth, phone_number
            """,
            (user.name, user.email, user.password_hash, user.date_of_birth, user.phone_number)
        )
        new_user = cursor.fetchone()
        conn.commit()
        return new_user
    except Exception as e:
        conn.rollback()
        print(f"Error creating user: {e}")
        raise
    finally:
        cursor.close()

def create_health_data(health_data: Health_data):
    if not conn:
        raise Exception("No database connection available.")
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(
            """
            INSERT INTO health_data (heart_rate, blood_pressure, oxygen_level, temperature, user_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING data_id, heart_rate, blood_pressure, oxygen_level, temperature, user_id
            """,
            (
                health_data.heart_rate,
                health_data.blood_pressure,
                health_data.oxygen_level,
                health_data.temperature,
                health_data.user_id
            )
        )
        new_health_data = cursor.fetchone()
        conn.commit()
        return new_health_data
    except Exception as e:
        conn.rollback()
        print(f"Error creating health data: {e}")
        raise
    finally:
        cursor.close()
        
# Function to create a new alert
def create_alert(alert: Alerts):
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO alerts (alert_type, message, status, user_id)
                VALUES (%s, %s, %s, %s)
                RETURNING alert_id, alert_type, message, status, user_id
                """,
                (alert.alert_type, alert.message, alert.status, alert.user_id)
            )
            new_alert = cursor.fetchone()
            conn.commit()
            return new_alert
    except Exception as e:
        conn.rollback()
        print(f"Error creating alert: {e}")
        return None

# Function to update health data for a user
def update_user_data_health(id_user, new_user_data_health: Health_data):
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE health_data 
                SET heart_rate = %s, 
                    blood_pressure = %s, 
                    oxygen_level = %s, 
                    temperature = %s
                WHERE user_id = %s 
                RETURNING heart_rate, blood_pressure, oxygen_level, temperature,user_id
                """,
                (
                    new_user_data_health.heart_rate,
                    new_user_data_health.blood_pressure,
                    new_user_data_health.oxygen_level,
                    new_user_data_health.temperature,
                    id_user
                )
            )
            updated_data_health = cursor.fetchone()
            conn.commit()
            return updated_data_health
    except Exception as e:
        conn.rollback()
        print(f"Error updating user health data: {e}")
        return None

# Function to get full user info
def get_user_full_info(email: str):
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT 
                    u.user_id, u.name, u.email, u.password_hash, u.phone_number, u.date_of_birth, u.doctor_id,
                    h.heart_rate, h.blood_pressure, h.oxygen_level, h.temperature,
                    r.id_recommendations, r.message AS recommendation_message,
                    a.alert_id, a.alert_type, a.message AS alert_message, a.status
                FROM users u
                LEFT JOIN health_data h ON u.user_id = h.user_id
                LEFT JOIN recommendations r ON u.user_id = r.user_id
                LEFT JOIN alerts a ON u.user_id = a.user_id
                WHERE u.email = %s
                """,
                (email,)
            )
            rows = cursor.fetchall()

            if not rows:
                return None

            # Regrouper les informations
            user_info = {
                "user_id": rows[0]["user_id"],
                "name": rows[0]["name"],
                "email": rows[0]["email"],
                "password_hash": rows[0]["password_hash"],
                "phone_number": rows[0]["phone_number"],
                "date_of_birth": rows[0]["date_of_birth"],
                "doctor_id": rows[0]["doctor_id"],
                "health_data": {
                    "heart_rate": rows[0]["heart_rate"],
                    "blood_pressure": rows[0]["blood_pressure"],
                    "oxygen_level": rows[0]["oxygen_level"],
                    "temperature": rows[0]["temperature"]
                },
                "recommendations": [],
                "alerts": []
            }
            existing_ids = {rec["id_recommendations"] for rec in user_info["recommendations"]}

            # Ajouter les recommandations et les alertes
            for row in rows:
                if row["id_recommendations"] and row["id_recommendations"] not in existing_ids:
                    user_info["recommendations"].append({
                        "id_recommendations": row["id_recommendations"],
                        "message": row["recommendation_message"]
                    })
                    existing_ids.add(row["id_recommendations"])
                if row["alert_id"]:
                    user_info["alerts"].append({
                        "alert_id": row["alert_id"],
                        "alert_type": row["alert_type"],
                        "message": row["alert_message"],
                        "status": row["status"]
                    })

            return user_info

    except Exception as e:
        print(f"Error retrieving full user information: {e}")
        return None


# Function to get doctor information based on user ID
def get_doctor_info(user_id):
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT d.name, d.email,d.password_hash, d.specialization, d.phone_number 
                FROM doctors d
                JOIN users u ON u.doctor_id = d.doctor_id
                WHERE u.user_id = %s
                """,
                (user_id,)
            )
            doctor_info = cursor.fetchone()
            return doctor_info
    except Exception as e:
        print(f"Error retrieving doctor's info: {e}")
        return None

# Function to create a new doctor (sign up)
def create_doctor(doctor: Doctor):
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO doctors (name, email, password_hash, specialization, phone_number)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING doctor_id, name, email,password_hash, specialization, phone_number
                """,
                (doctor.name, doctor.email, doctor.password_hash, doctor.specialization, doctor.phone_number)
            )
            new_doctor = cursor.fetchone()
            conn.commit()
            return new_doctor
    except Exception as e:
        conn.rollback()
        print(f"Error creating doctor: {e}")
        return None

#Retrive doctor's info
def doctor_info(doctor_email):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        # Execute the query to fetch user information by email
        cursor.execute(
            """
            SELECT * FROM doctors WHERE email = %s
            """,
            (doctor_email,)
        )
        # Fetch the user's information
        doctor_info = cursor.fetchone()
        return doctor_info
    except Exception as e:
        print(f"Error retrieving user info: {e}")
        return None
    finally:
        cursor.close()
        
# Retrieve all the users' info of a doctor
def get_user_details_by_doctor(doctor_id: int):
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Fetch all users along with their health data and alerts using JOINs
            cursor.execute(
                """
                SELECT 
                    u.user_id, u.name, u.email, u.phone_number, u.date_of_birth, u.doctor_id,
                    h.heart_rate, h.blood_pressure, h.oxygen_level, h.temperature,
                    a.alert_type, a.message, a.status
                FROM users u
                LEFT JOIN health_data h ON u.user_id = h.user_id
                LEFT JOIN alerts a ON u.user_id = a.user_id
                WHERE u.doctor_id = %s
                """,
                (doctor_id,)
            )

            # Fetch all the results
            results = cursor.fetchall()
            return results

    except Exception as e:
        print(f"Error retrieving user details: {e}")
        return None


# Function to update the alerts table when a doctor sees the alert of a user
def update_alert(alert_id: int, updated_alert: Alerts):
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Execute the update query to modify the alert details
            cursor.execute(
                """
                UPDATE alerts
                SET alert_type = %s,
                    message = %s,
                    status = %s
                WHERE alert_id = %s
                RETURNING alert_id, alert_type, message, status, user_id
                """,
                (
                    updated_alert.alert_type,
                    updated_alert.message,
                    updated_alert.status,
                    alert_id
                )
            )

            # Fetch the updated record
            updated_alert_record = cursor.fetchone()
            conn.commit()

            # Return the updated alert
            return updated_alert_record

    except Exception as e:
        print(f"Error updating alert: {e}")
        conn.rollback()
        return None

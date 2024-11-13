import streamlit as st

import requests

# Base URL for the FastAPI server
BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="Medical System", page_icon="🌻", layout="centered")

# Helper function to create a new user
def create_user(user_data, user_type):
    if user_type == "Patient":
        url = f"{BASE_URL}/user/create_user"
    else:
        url = f"{BASE_URL}/doctor/create_doctor"
    response = requests.post(url, json=user_data)
    return response.json()

# Helper function to authenticate user
def login_user(email, password, user_type):
    if user_type == "Patient":
        url = f"{BASE_URL}/user/get_user_full_info"
    else:
        url = f"{BASE_URL}/doctor/get_doctor_info"
    response = requests.get(url, params={"email": email})

    if response.status_code == 200:
        user_info = response.json()
        st.write(user_info)
        if user_info["password_hash"] == password:
            return user_info
    return None

# Helper function to fetch user profile data
def get_user_info(user_type, email):
    if user_type == "Patient":
        url = f"{BASE_URL}/user/get_user_full_info"
    else:
        url = f"{BASE_URL}/doctor/get_doctor_info"
    response = requests.get(url, params={"email": email})
    return response.json() if response.status_code == 200 else None

def update_health_data(user_id,health_data):
    
    url = f"{BASE_URL}/user/update_health_data/{user_id}"
    try:
        response = requests.put(url, json=health_data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to update health data. Status code: {response.status_code}, Response: {response.text}")
            return None
    except Exception as e:
        print(f"Error updating health data: {e}")
        return None


# Helper function to retrieve all patients assigned to a doctor
def get_users_by_doctor(doctor_id):

    url = f"{BASE_URL}/doctors/get_users_by_doctor/{doctor_id}"
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

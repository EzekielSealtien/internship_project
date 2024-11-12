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

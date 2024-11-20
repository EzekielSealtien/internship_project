import streamlit as st
import bcrypt
from Client.Functions_ import talk_with_server as tws
def show_signup_doctor_page():
    st.title("Sign Up")

    with st.form("sign_up_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        phone_number = st.text_input("Phone Number")
        date_of_birth = st.text_input("Date of Birth")
        specialization = st.text_input("Specialization")
    
        submit = st.form_submit_button("Register")

        if submit:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            user_data = {
                "name": name,
                "email": email,
                "password_hash": hashed_password,
                "date_of_birth": date_of_birth,
                "phone_number": phone_number,
                "specialization":specialization
            }

            response = tws.create_doctor(user_data)
            if "doctor_id" in response:
                st.session_state["email"] = email
                st.query_params.update(page="login_doctor")
                st.rerun()
            else:
                st.error("Registration failed.")

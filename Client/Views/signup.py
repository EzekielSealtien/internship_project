import streamlit as st
import bcrypt
from Client.Functions_ import talk_with_server as tws


    
def show_signup_page():
    st.title("Sign Up")
    user_type = st.selectbox("Are you a:", ["Patient", "Doctor"])

    with st.form("sign_up_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        phone_number = st.text_input("Phone Number")
        date_of_birth = st.text_input("Date of Birth")
        if user_type == "Doctor":
            specialization = st.text_input("Specialization")
        
        submit = st.form_submit_button("Register")

        if submit:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            user_data = {
                "name": name,
                "email": email,
                "password_hash": hashed_password,
                "date_of_birth": date_of_birth,
                "phone_number": phone_number
            }
            if user_type == "Doctor":
                user_data["specialization"] = specialization
                if "date_of_birth" in user_data:
                    del user_data["date_of_birth"]
            
            response = tws.create_user(user_data, user_type)
            if "user_id" in response or "doctor_id" in response:
                st.success("Registration successful! Please log in.")
                st.session_state["email"] = email
                st.session_state["user_type"] = user_type
                st.query_params.update(page="login")
                st.rerun()
            else:
                st.error("Registration failed.")

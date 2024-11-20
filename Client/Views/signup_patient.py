import streamlit as st
import bcrypt
from Client.Functions_ import talk_with_server as tws


    
def show_signup_patient_page():
    st.title("Sign Up")

    with st.form("sign_up_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        phone_number = st.text_input("Phone Number")
        date_of_birth = st.text_input("Date of Birth")

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
        
            response = tws.create_patient(user_data)
            if "user_id"  in response:
                st.success("Registration successful! Please log in.")
                st.session_state["email"] = email
                st.query_params.update(page="login_patient")
                st.rerun()
            else:
                st.error("Registration failed.")
                
    col1,col2=st.columns([6,4])
    with col2:
        if st.button('sign up as a doctor'):
                st.query_params['page']='signup_doctor'
                st.rerun()

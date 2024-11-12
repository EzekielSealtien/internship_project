import streamlit as st
from Client.Functions_ import talk_with_server as tws


def show_profile_page():
    st.title("User Profile")
    email = st.session_state.get("email")
    user_type = st.session_state.get("user_type")

    if not email or not user_type:
        st.error("You are not logged in.")
        st.stop()

    user_info = tws.get_user_info(user_type, email)
    
    if user_info:
        st.subheader(f"Welcome, {user_info['name']}!")
        st.write(f"**Email**: {user_info['email']}")
        st.write(f"**Phone Number**: {user_info['phone_number']}")

        if user_type == "Patient":
            health_data=user_info['health_data']
            st.write("### Health Data")
            st.write(f"Heart Rate: {health_data['heart_rate']}")
            st.write(f"Blood Pressure: {health_data['blood_pressure']}")
            st.write(f"Oxygen Level: {health_data['oxygen_level']}")
            st.write(f"Temperature: {health_data['temperature']}")
            
            
            st.write("### Alerts")
            for alert in user_info["alerts"]:
                st.write(f"- {alert['alert_type']}: {alert['message']} (Status: {alert['status']})")
                
            st.write("### Recommendations")
            for recommendation in user_info["recommendations"]:
                st.write(f"- {recommendation['id_recommendations']}: {recommendation['message']}")
        
        elif user_type == "Doctor":
            if user_info["specialization"]:
                st.write(f"**Specialization**: {user_info['specialization']}")
    else:
        st.error("Failed to load profile information.")

def show_login_page():
    st.title("Login")
    user_type = st.selectbox("Are you a:", ["Patient", "Doctor"])

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            user_info = tws.login_user(email, password, user_type)
            if user_info:
                st.success("Login successful!")
                st.session_state["email"] = email
                st.session_state["user_type"] = user_type
                st.session_state["user_info"] = user_info
                st.experimental_set_query_params(page="profile")
                st.rerun()
            else:
                st.error("Invalid credentials.")

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
            user_data = {
                "name": name,
                "email": email,
                "password_hash": password,
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
                st.experimental_set_query_params(page="login")
                st.rerun()
            else:
                st.error("Registration failed.")

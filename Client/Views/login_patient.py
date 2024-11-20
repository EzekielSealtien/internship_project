import streamlit as st
from Client.Functions_ import talk_with_server as tws



def show_login_patient_page():
    st.title("Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            user_info = tws.login_patient(email, password)
            if user_info:
                st.success("Login successful!")
                st.session_state["email"] = email
                st.session_state["user_info"] = user_info
                st.query_params['page']="home_page_patient"
                st.rerun()
            else:
                st.error("Invalid credentials.")
    col1,col2=st.columns([6,4])
    with col2:
        col3,col4=st.columns([4,6])
        with col3:
            if st.button('Sign up'):
                st.query_params['page']='signup_patient'
                st.rerun()
        with col4:
            if st.button('Log in as a doctor'):
                st.query_params['page']='login_doctor'
                st.rerun()
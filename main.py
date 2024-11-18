import streamlit as st
from Client.Views.add_patient import show_add_patient_page
from Client.Views.signup_patient import show_signup_patient_page
from Client.Views.signup_doctor import show_signup_doctor_page
from Client.Views.login_patient import show_login_patient_page
from Client.Views.login_doctor import show_login_doctor_page
from Client.Views.profil_patient import show_profile_patient_page
from Client.Views.profil_doctor import show_profile_doctor_page
from Client.Views.home_page_patient import show_home_page_patient
from Client.Views.home_page_doctor import show_home_page_doctor

page =  st.query_params.get("page", ["login"])
if page == "profile_patient":
    show_profile_patient_page()
elif page == "profil_doctor":
    show_profile_doctor_page()
elif page == "signup_patient":
    show_signup_patient_page()
elif page == "signup_doctor":
    show_signup_doctor_page()
elif page == "login_patient":
    show_login_patient_page()
elif page == "login_doctor":
    show_login_doctor_page() 
elif page == "add_patient":
    show_add_patient_page()
elif page == "home_page_patient":
    show_home_page_patient() 
elif page == "home_page_doctor":
    show_home_page_doctor()
else:
    show_login_patient_page()



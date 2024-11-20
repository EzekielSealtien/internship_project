import streamlit as st
import Client.Views_.add_patient as show_add_patient_page
import Client.Views_.signup_patient as show_signup_patient_page
import Client.Views_.signup_doctor as show_signup_doctor_page
import Client.Views_.login_patient as show_login_patient_page
import Client.Views_.login_doctor as show_login_doctor_page
import Client.Views_.profil_patient as show_profile_patient_page
import Client.Views_.profil_doctor as show_profile_doctor_page
import Client.Views_.home_page_patient as show_home_page_patient
import Client.Views_.home_page_doctor as show_home_page_doctor



page =  st.query_params.get("page", ["login"])
if page == "profile_patient":
    show_profile_patient_page.show_profile_patient_page()
elif page == "profil_doctor":
    show_profile_doctor_page.show_profile_doctor_page()
elif page == "signup_patient":
    show_signup_patient_page.show_signup_patient_page()
elif page == "signup_doctor":
    show_signup_doctor_page.show_signup_doctor_page()
elif page == "login_patient":
    show_login_patient_page.show_login_patient_page()
elif page == "login_doctor":
    show_login_doctor_page.show_login_doctor_page() 
elif page == "add_patient":
    show_add_patient_page.show_add_patient_page()
elif page == "home_page_patient":
    show_home_page_patient.show_home_page_patient() 
elif page == "home_page_doctor":
    show_home_page_doctor.show_home_page_doctor()
else:
    show_login_patient_page.show_login_patient_page()



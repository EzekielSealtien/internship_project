import streamlit as st
from Client.Views import view
from Client.Views.login import show_login_page
from Client.Views.signup import show_signup_page
from Client.Views.profil import show_profile_page
from Client.Views.add_patient import show_add_patient_page




page =  st.query_params.get("page", ["login"])

if page == "profile":
    show_profile_page()
elif page == "signup":
    show_signup_page()
elif page == "home":
    view.show_home_page()
elif page == "add_patient":
    show_add_patient_page()
else:
    show_login_page()



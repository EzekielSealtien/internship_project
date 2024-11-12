import streamlit as st
from Client.Views import view


page = st.experimental_get_query_params().get("page", ["login"])[0]

if page == "profile":
    view.show_profile_page()
elif page == "signup":
    view.show_signup_page()
else:
    view.show_login_page()



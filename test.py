import streamlit as st


# Button to send a message
if st.button("Send Message"):
    # Display a toast notification
    st.toast("report sent successfully!")

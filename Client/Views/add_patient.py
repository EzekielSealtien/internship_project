import streamlit as st
from Client.Functions_ import talk_with_server as tws



def show_add_patient_page():
    doctor_id=st.session_state.user_info['doctor_id']
    with st.form(key='add_patient'):
        name=st.text_input("Patient's name:")
        email=st.text_input("Patient's email:")
        submit=st.form_submit_button('Add patient:')
        if submit:
            print(f"------------->{type(email)}")
            print(f"------------>{type(doctor_id)}")
            response=tws.assign_doctor_to_user(email,doctor_id)
            if response:
                st.toast("Patient added successfully!")

    col11, col21, col31 = st.columns([1, 2, 1])
    with col21:
        if st.button("Return to the Home Page"):
            st.query_params.update(page="home")
            st.rerun()

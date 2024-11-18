import streamlit as st 
from Client.Functions_ import talk_with_server as tws
def show_profile_doctor_page():
    # Set page background color
    st.markdown(
        """
        <style>
        .main {
            background-color: #e0f7da;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("📝 Profil Utilisateur")
    email = st.session_state.get("email")

    if not email:
        st.error("Vous n'êtes pas connecté.")
        st.stop()

    # Fetch user information
    user_info = tws.get_doctor_info(email)
    
    if user_info:
        # Display welcome message
        st.markdown(f"<h2 style='text-align: center;'>👤 Bienvenue, {user_info['name']}!</h2>", unsafe_allow_html=True)
        
        # Create two columns
        col1, col2 = st.columns([7, 3])

        # Column 1: User Information
        with col1:
            st.subheader(" Informations Utilisateur")
            st.write(f" Email: {user_info['email']}")
            st.write(f" Téléphone: {user_info['phone_number']}")

        # Column 2: Doctor Information
        with col2:
            st.subheader("🩺 Informations Spécialisation")
            st.write(f"**Spécialisation**: {user_info['specialization']}")
    else:
        st.error("Erreur lors du chargement des informations du profil.")
        
    col11, col21, col31 = st.columns([1, 2, 1])
    with col21:
        if st.button("Return to the Home Page"):
            st.query_params.update(page="home_page_doctor")
            st.rerun()
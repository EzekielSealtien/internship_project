import streamlit as st 
from Client.Functions_ import talk_with_server as tws


def show_profile_page():
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
    user_type = st.session_state.get("user_type")

    if not email or not user_type:
        st.error("Vous n'êtes pas connecté.")
        st.stop()

    # Fetch user information
    user_info = tws.get_user_info(user_type, email)
    
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
            if user_type == "Patient":
                st.write(f" Date de Naissance: {user_info['date_of_birth']}")
                st.write("### 💊 Données de Santé")
                health_data = user_info['health_data']
                
                    

                # Editable health data fields
                heart_rate = st.number_input("Heart Rate ", value=14)
                blood_pressure = st.number_input("Blood Pressure ", value=50)
                oxygen_level = st.number_input("Oxygen Level ", value=90)
                temperature = st.number_input("Temperature ", value=37)



                # Button to update or create health data
                if st.button("Mettre à jour les données de santé"):
                    updated_data = {
                        "heart_rate": heart_rate,
                        "blood_pressure": blood_pressure,
                        "oxygen_level": oxygen_level,
                        "temperature": temperature,
                        "user_id":user_info['user_id']
                    }
                    if health_data['heart_rate']==None:
                        response=tws.create_health_data(updated_data)
                    else:
                        response = tws.update_health_data(updated_data)
                    
                    if response:
                        st.toast("Health data updated  successfully!")

                    else:
                        st.error("Erreur lors de la mise à jour des données de santé.")

        # Column 2: Doctor Information
        with col2:
            if user_type == "Patient":
                st.subheader("🩺 Informations du Docteur")
                st.write(f"**👨‍⚕️ Suivi par  Docteur**: {user_info['doctor_name']}")
                st.write(f"**📞 Téléphone**: {user_info['doctor_phone_number']}")
                st.write(f"**✉️ Email**: {user_info['doctor_email']}")
                st.write(f"**🎓 Spécialisation**: {user_info['doctor_specialization']}")

                # Button to call the doctor (hypothetical functionality)
                if st.button("📞 Appeler le Docteur"):
                    doctor_whatsapp_number = f"+1{user_info['doctor_phone_number']}"
                    st.success(f"[Appel en cours](https://wa.me/{doctor_whatsapp_number})")

            
            elif user_type == "Doctor":
                st.subheader("🩺 Informations Spécialisation")
                st.write(f"**Spécialisation**: {user_info['specialization']}")
    else:
        st.error("Erreur lors du chargement des informations du profil.")
        
    col11, col21, col31 = st.columns([1, 2, 1])
    with col21:
        if st.button("Return to the Home Page"):
            st.query_params.update(page="home")
            st.rerun()
import streamlit as st
from Client.Functions_ import talk_with_server as tws


def show_home_page():
    # Style of the page
    st.markdown("""
        <style>
        .stApp {
            background-color: #add8e6; /* Light blue background */
        }
        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .profile-button {
            background-color: #007bff;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            cursor: pointer;
        }
        .patient-frame {
            border: 2px solid #007bff;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            background-color: #f0f8ff;
        }
        </style>
    """, unsafe_allow_html=True)

    user_info = st.session_state.get("user_info", None)
    if not user_info:
        st.error("You are not logged in.")
        st.stop()

    # Welcome message
    st.markdown(f"<h1 style='text-align: center;'>Bienvenue {user_info['name']} </h1>", unsafe_allow_html=True)
    
    # Profile and logout buttons
    col1, col2 = st.columns([6, 4])
    with col2:
        col3, col4 = st.columns([4, 5])
        with col3:
            if st.button("Voir profil", key="profile_button"):
                st.experimental_set_query_params(page="profile")
                st.rerun()
        with col4:
            if st.button("🔒 Deconnexion", key="deconnexion_button"):
                st.session_state.clear()
                st.session_state["is_logged_in"] = False
                st.success("Vous êtes maintenant déconnecté.")
                st.experimental_set_query_params(page="login")
                st.rerun()

    user_type = st.session_state.user_type

    # If the user is a doctor, display their patients
    if user_type == "Doctor":
        st.subheader("👩‍⚕️ Patients Associés")
        
        # Fetch patients' details associated with the doctor
        doctor_id = user_info.get('doctor_id')
        patients = tws.get_users_by_doctor(doctor_id)

        if not patients:
            st.info("Aucun patient associé.")
        else:
            # Display each patient in a frame
            for patient in patients:
                with st.container():
                    st.markdown("<div class='patient-frame'>", unsafe_allow_html=True)
                    
                    # Patient details
                    st.write(f"**Nom**: {patient['name']} ")
                    st.write(f"**Téléphone**: {patient['phone_number']} ")
                    st.write(f"**Email**: {patient['email']} 📧")
                    st.write(f"**Date de Naissance**: {patient['date_of_birth']} ")
                    
                    # Health data
                    health_data = patient.get('health_data', {})
                    st.write("###  Données de Santé")
                    st.write(f"Fréquence Cardiaque: {health_data.get('heart_rate', 'N/A')}")
                    st.write(f"Pression Artérielle: {health_data.get('blood_pressure', 'N/A')}")
                    st.write(f" Niveau d'Oxygène: {health_data.get('oxygen_level', 'N/A')}")
                    st.write(f" Température: {health_data.get('temperature', 'N/A')}")
                    
                    # Alerts
                    st.write("### 📢 Alertes")
                    alerts = patient.get("alerts", [])
                    if alerts:
                        for alert in alerts:
                            st.write(f"- {alert['alert_type']} ⚠️: {alert['message']} (Status: {alert['status']})")
                    else:
                        st.write("Aucune alerte pour ce patient.")

                    # WhatsApp call button
                    patient_whatsapp_number = f"+1{patient['phone_number']}"
                    if st.button(f"📞 Appeler {patient['name']}", key=f"call_{patient['user_id']}"):
                        st.success(f"[Lancer un appel WhatsApp](https://wa.me/{patient_whatsapp_number})")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
    else:
        # For patients, display their alerts and recommendations
        st.write("### 📢 Alertes")
        for alert in user_info.get("alerts", []):
            st.write(f"- {alert['alert_type']} ⚠️: {alert['message']} (Status: {alert['status']})")

        st.write("### 💡 Recommandations")
        for recommendation in user_info.get("recommendations", []):
            st.write(f"- {recommendation['id_recommendations']} : {recommendation['message']}")

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
                heart_rate = st.number_input("Heart Rate ", value=health_data.get('heart_rate', 0))
                blood_pressure = st.number_input("Blood Pressure ", value=health_data.get('blood_pressure', 0))
                oxygen_level = st.number_input("Oxygen Level ", value=health_data.get('oxygen_level', 0))
                temperature = st.number_input("Temperature ", value=health_data.get('temperature', 0))

                # Button to update health data
                if st.button("Mettre à jour les données de santé"):
                    updated_data = {
                        "heart_rate": heart_rate,
                        "blood_pressure": blood_pressure,
                        "oxygen_level": oxygen_level,
                        "temperature": temperature
                    }
                    response = tws.update_health_data(user_info['user_id'], updated_data)
                    if response:
                        st.success("Données de santé mises à jour avec succès! 🎉")
                        st.rerun()
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
            st.experimental_set_query_params(page="home")
            st.rerun()

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
                st.experimental_set_query_params(page="home")
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

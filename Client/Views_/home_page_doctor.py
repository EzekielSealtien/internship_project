import streamlit as st
from Client.Functions_ import talk_with_server as tws

def show_home_page_doctor():
    
    if 'button_mark_as_read' not in st.session_state:
        st.session_state.button_mark_as_read="button_mark_as_read"
    
    # Style of the page
    st.markdown("""
        <style>
        .stApp {
            background-color: #add8e6;
        }
        .patient-frame {
            border: 2px solid #007bff;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            background-color: #f0f8ff;
        }
        .profile-button {
            background-color: #007bff;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            cursor: pointer;
        }
        </style>
    """, unsafe_allow_html=True)
    
    user_info = st.session_state.get("user_info", None)
    if not user_info:
        st.error("You are not logged in.")
        st.stop()

    st.markdown(f"<h1 style='text-align: center;'>Welcome, {user_info['name']} </h1>", unsafe_allow_html=True)
    

    # Profile and Logout Buttons
    col1, col2 = st.columns([4, 6])
    with col2:
        col3, col4,col5 = st.columns([2,4,4])
        with col3:
            if st.button("Profil", key="profile_button"):
                st.query_params['page']="profil_doctor"
                st.rerun()
        with col4:
            if st.button("➕ Add patient",key="add_patient"):
                st.query_params.update(page="add_patient")
                st.rerun()
        
        with col5:
            if st.button("🔒 Deconnexion", key="deconnexion_button"):
                st.session_state.clear()
                st.session_state["is_logged_in"] = False
                st.success("Vous êtes maintenant déconnecté.")
                st.query_params.update(page="login_doctor")
                st.rerun()
 

    st.subheader("👩‍⚕️ Patients Associés")
    
    # Fetch patients' details associated with the doctor
    doctor_id = user_info.get('doctor_id')
    patients = tws.get_users_by_doctor(doctor_id)

    if not patients:
        st.info("Aucun patient associé.")
    else:
        for patient in patients:
            with st.container():
                st.markdown("<div class='patient-frame'>", unsafe_allow_html=True)
                st.write(f"**Nom**: {patient['name']}")
                st.write(f"**Téléphone**: {patient['phone_number']}")
                st.write(f"**Email**: {patient['email']} 📧")
                st.write(f"**Date de Naissance**: {patient['date_of_birth']}")

                # Health data
                health_data = patient.get('health_data', {})
                st.write("### Données de Santé")
                st.write(f"Fréquence Cardiaque: {health_data.get('heart_rate', 'N/A')}")
                st.write(f"Pression Artérielle: {health_data.get('blood_pressure', 'N/A')}")
                st.write(f"Niveau d'Oxygène: {health_data.get('oxygen_level', 'N/A')}")
                st.write(f"Température: {health_data.get('temperature', 'N/A')}")

                # Alerts
                st.write("### 📢 Alerts")
                
                alerts = patient.get("alerts", [])
                recommendations = patient.get("recommendations", [])
                rec_id=1
                id__recommendaton=1
                recommendation_message=""


                col8,col10,col11=st.columns([3,3,4])
                
                for alert in alerts:
                    
                    alert_id=alert['alert_id']
                    #col8
                    with col8:
                        message=alert['message']
                        mes=message[8:-1]
                        st.markdown(f"- {alert['alert_type']}: affected by {mes} <br>  ", unsafe_allow_html=True)

                    #col10
                    with col10:
                        for recommendation in recommendations:
                            if recommendation["alert_id"] == alert["alert_id"]:
                                rec_id=recommendation["alert_id"]
                                id__recommendaton=recommendation['id_recommendations']
                                recommendation_message=recommendation['message']


                        with st.expander("Recommendations",expanded=False):
                            st.markdown(recommendation_message,unsafe_allow_html=True)
                            mark_as_read_key=f"{user_info.get("user_id")}{alert['alert_id']}{rec_id}"
                            if st.button("Mark as read",key=mark_as_read_key):
                                new_status="Consulted"
                                updated_alert = {
                                    "alert_type": alert['alert_type'],
                                    "message": alert['message'],
                                    "status": new_status,
                                    "user_id": patient.get("user_id")
                                }
                                tws.update_alert(alert_id,updated_alert)
                                st.toast("Notification sent successfully")
                    #col11               
                    with col11:
                        with st.expander("Write report",expanded=False, icon="💡"):
                            text_area_key=f"{user_info.get("user_id")}{alert['alert_id']}{rec_id}00"

                            doctor_report=st.text_area(label="Write",value="",key=text_area_key)  

                            send_key=f"{user_info.get("user_id")}{alert['alert_id']}{rec_id}0000"
                            if st.button("▶ **Send**",key=send_key):
                                updated_recommendation = {
                                    "message": recommendation_message,
                                    "alert_id": alert['alert_id'],
                                    "user_id": patient.get("user_id"),
                                    "doctor_report":doctor_report
                                }
                                tws.update_recommendation(id__recommendaton,updated_recommendation)
                                st.toast("report sent successfully!")

                                                
                # WhatsApp call button
                patient_whatsapp_number = f"+1{patient['phone_number']}"
                if st.button(f"📞 Appeler {patient['name']}", key=f"call_{patient['user_id']}"):
                    st.success(f"[Lancer un appel WhatsApp](https://wa.me/{patient_whatsapp_number})")
                    print(patient_whatsapp_number)
                    print(type(patient_whatsapp_number))
                
                st.markdown("</div>", unsafe_allow_html=True)


import streamlit as st
from Client.Functions_ import talk_with_server as tws
#For generate unique key


st.query_params
def show_home_page_patient():
    
    if 'disease_name' not in st.session_state:
        st.session_state.disease_name=""
    if 'disease_description' not in st.session_state:
        st.session_state.disease_description=""
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations=[]
    if "check" not in st.session_state:
        st.session_state.check=False
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
        col3,col5 = st.columns([4,6])
        with col3:
            if st.button("Profil", key="profile_button"):
                st.query_params['page']="profile_patient"

                st.rerun()
        with col5:
            if st.button("🔒 Deconnexion", key="deconnexion_button"):
                st.session_state.clear()
                st.session_state["is_logged_in"] = False
                st.success("Vous êtes maintenant déconnecté.")
                st.query_params['page']="login_patient"

                st.rerun()
            


    user_info = tws.get_updated_user(st.session_state["email"])

    # For patients, display their alerts and recommendations
    alerts = user_info.get("alerts", [])
    recommendations = user_info.get("recommendations", [])
    doctor_report=""
    
    st.write("### 📢 Alerts")
    for alert in alerts:
        st.markdown(f"**Alert Type**: {alert['alert_type']} ⚠️")
        st.markdown(f"**Message**: {alert['message']}")
        rec_id=1
        col5,col6=st.columns([6,4])
        with col5:
            st.write("💡 **Recommendations**:")
            for recommendation in recommendations:
                if recommendation["alert_id"] == alert["alert_id"]:
                    rec_id=recommendation["alert_id"]
                    st.markdown(f"- {recommendation['message']}")
                    doctor_report=recommendation['doctor_report']
        with col6:
            if alert['status']=="new alert":
                st.markdown(f"**Not consulted**")
            else:
                st.success("Consulted")
            
            key_download=f"key{alert["alert_id"]}"
            if type(doctor_report)==str:
                if len(doctor_report)>1:
                    st.download_button(
                        label="Download Doctor report",
                        key=key_download,
                        data=doctor_report,
                        file_name="Rapport_du_medecin",
                        mime='text/plain'
                    )

            #If the patient is cured
            if st.button('Cured',key=alert["alert_id"]):
                st.success("Cured")
                tws.delete_alert(alert["alert_id"])
                
                # Refresh the user's session
                email = st.session_state["email"]
                st.session_state.user_info = tws.get_updated_user(email)
                st.rerun()
        st.markdown("---")


    # Disease prediction for patients
    st.write("### Predict Disease")
    symptoms_list = [
        "itching", "skin rash", "nodal skin eruptions", "continuous sneezing",
        "shivering", "chills", "joint pain", "stomach pain", "acidity",
        "ulcers on tongue", "muscle wasting", "vomiting", "burning micturition",
        "spotting urination", "fatigue", "weight gain", "anxiety",
        "cold hands and feet", "mood swings", "weight loss", "restlessness"
    ]

    selected_symptoms = st.multiselect("Select your symptoms:", symptoms_list)
    list_of_17_symptoms = selected_symptoms + [0] * (17 - len(selected_symptoms))
    list_of_17_symptoms = list_of_17_symptoms[:17]

    if st.button("Predict Disease"):
        if not selected_symptoms:
            st.warning("Please select at least one symptom.")
        else:
            # Send symptoms to FastAPI for prediction
            result = tws.predict_disease(list_of_17_symptoms)
            
            if result:
                st.subheader("🩺 Disease Prediction Result")
                st.session_state.disease_name=result['disease_name']
                st.session_state.disease_description=result['disease_description']
                st.session_state.check=True

                myList=[]
                for rec in result['recommendations']:
                    myList.append(rec)
                
                st.session_state.recommendations=myList

                alert_data = {
                    "alert_type": "Danger",
                    "message": f"You have {result['disease_name']}",
                    "status": "new alert",
                    "user_id": user_info.get("user_id")
                }
                new_alert = tws.create_alert(alert_data)
                if new_alert:
                    alert_id = new_alert.get("alert_id")
                    combined_recommendations = " ; ".join(result['recommendations'])
                    recommendation_data = {
                        "message": combined_recommendations,
                        "alert_id": alert_id,
                        "user_id": user_info.get("user_id"),
                        "doctor_report":""
                    }
                    tws.create_recommendation(recommendation_data)
                
                # Refresh the user's session
                email = st.session_state["email"]
                st.session_state.user_info = tws.get_updated_user(email)
                st.rerun()
            
                
    #If the predict's buttton has been clicked
    if st.session_state.check: 
        st.subheader("🩺 Disease Prediction Result")
        st.write(f"**Disease Name**: {st.session_state.disease_name}")
        st.write(f"**Description**: {st.session_state.disease_description}")
        
        st.subheader("💡 Recommended Precautions")
        for rec in st.session_state.recommendations:
            st.write(f"- {rec}")


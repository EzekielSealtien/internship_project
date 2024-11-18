import Functions_.commands as cmd
from fastapi import FastAPI, HTTPException
from typing import Optional, List
from Functions_.model import predd
import pickle


app = FastAPI()
base_url = "http://localhost:8000"
path="./Functions_/downloaded-model/skops-iw9h_jza.pkl"


# Route to create a new    
@app.post("/user/create_user", response_model=Optional[cmd.UserResponse])
def create_new_user(user: cmd.Users):
    try:
        new_user = cmd.create_user(user)
        if not new_user:
            raise HTTPException(status_code=400, detail="User could not be created")
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")


# Route to get full user info including health data, recommendations, and alerts   
@app.get("/user/get_user_full_info")
def get_all_info_user(email: str):
    try:
        infos_user = cmd.get_user_full_info(email)
        if infos_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return infos_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user's info: {str(e)}")


# Route to update health data for a user 
@app.put("/user/update_health_data", response_model=Optional[cmd.Health_data])
def update_user_health_data(health_data: cmd.Health_data):
    try:
        updated_data = cmd.update_user_data_health(health_data)
        if updated_data is None:
            raise HTTPException(status_code=400, detail="Failed to update health data")
        return updated_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating health data: {str(e)}")


# Route to create a new health data record  
@app.post("/user/create_health_data", response_model=Optional[cmd.Health_dataRespons])
def create_health_data(health_data: cmd.Health_data):
    try:
        new_health_data = cmd.create_health_data(health_data)
        if new_health_data is None:
            raise HTTPException(status_code=400, detail="Failed to create health data")
        return new_health_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating health data: {str(e)}")


# Route to create a new alert  
@app.post("/user/create_alert", response_model=Optional[cmd.AlertsResponse])
def create_alert(alert: cmd.Alerts):
    try:
        new_alert = cmd.create_alert(alert)
        if new_alert is None:
            raise HTTPException(status_code=400, detail="Failed to create alert")
        return new_alert
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating alert: {str(e)}")


@app.post("/user/create_recommendation", response_model=Optional[cmd.recommendationResponse])
def create_recommendation(recommendation: cmd.recommendation):
    try:
        new_recommendation = cmd.create_recommendation(recommendation)
        if new_recommendation is None:
            raise HTTPException(status_code=400, detail="Failed to create recommendation")
        return new_recommendation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating recommendation: {str(e)}")
    
    
# Route to update an alert  
@app.put("/user/update_alert/{alert_id}")
def update_alert(alert_id: int, updated_alert: cmd.Alerts):
    try:
        updated_alert_record = cmd.update_alert(alert_id, updated_alert)
        if updated_alert_record is None:
            raise HTTPException(status_code=404, detail="Alert not found or could not be updated")
        return updated_alert_record
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating alert: {str(e)}")

@app.put("/user/update_recommendation/{id_recommendations}")
def update_recommendation(id_recommendations: int, updated_recommendation: cmd.recommendation):
    try:
        updated_recommendation_record = cmd.update_recommendation(id_recommendations, updated_recommendation)
        if updated_recommendation_record is None:
            raise HTTPException(status_code=404, detail="Recommendation not found or could not be updated")
        return updated_recommendation_record
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating recommendation: {str(e)}")

@app.put("/user/assign_doctor")
def assign_doctor_to_user(doctor_assignment: cmd.DoctorAssignment):
    try:
        updated_user = cmd.update_user_doctor(doctor_assignment)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found or could not update doctor assignment")
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user's doctor assignment: {str(e)}")

# Route to create a new doctor  
@app.post("/doctor/create_doctor", response_model=Optional[cmd.DoctorResponse])
def create_new_doctor(doctor: cmd.Doctor):
    try:
        new_doctor = cmd.create_doctor(doctor)
        if new_doctor is None:
            raise HTTPException(status_code=400, detail="Doctor could not be created")
        return new_doctor
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating doctor: {str(e)}")


# Route to get doctor's   
@app.get("/doctor/get_doctor_info", response_model=Optional[cmd.DoctorResponse])
def get_doctor_info(email: str):
    try:
        doctor_info = cmd.doctor_info(email)
        if doctor_info is None:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return doctor_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving doctor's info: {str(e)}")

# Route to get doctor's info by user's ID  
@app.get("/user/get_doctor_info/{user_id}", response_model=Optional[cmd.Doctor])
def get_doctor_info_by_user_id(user_id: int):
    try:
        doctor_info = cmd.get_doctor_info(user_id)
        if doctor_info is None:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return doctor_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving doctor's info: {str(e)}")


# Route to get all users assigned to a doctor  
@app.get("/doctors/get_users_by_doctor/{doctor_id}")
def get_users_by_doctor(doctor_id: int):
    try:
        users_info = cmd.get_user_details_by_doctor(doctor_id)
        if not users_info:
            raise HTTPException(status_code=404, detail="No users found for this doctor")
        return users_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving users' info: {str(e)}")

@app.delete("/user/delete_alert/{alert_id}")
def delete_alert(alert_id: int):
    try:
        deleted_alert = cmd.delete_alert(alert_id)
        if deleted_alert:
            return {"message": "Alert deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Alert not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting alert: {str(e)}")


#Route for predicting the disease based on symptoms
@app.post("/predict_disease")
def predict_disease(list_symptoms:cmd.SymptomsRequest):
    pickled_model=pickle.load(open(path,'rb'))
    try:
        response=predd(pickled_model,list_symptoms.list_symptoms)
        if not response:
            raise HTTPException(status_code=404, detail="No disease detected")
        return response
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error predicting the disease : info:{str(e)}")
        
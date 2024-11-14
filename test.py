import streamlit as st

value=st.text_area(label="Write",value="")
print(value)

if st.button('report'):
    print("yes")
    

if doctor_report!="":
    st.download_button(
        label="Doctor report",
        key=doctor_report_key,
        data=doctor_report,
        file_name='rapport_du_medcin.pdf',
        mime='text/plain'
    )
    
                    doctor_report_key=f"doctor_report{user_info.get("user_id")}{alert.get("alert_id")}"

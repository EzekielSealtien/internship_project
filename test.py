import streamlit as st


if st.button('report'):
    st.session_state.report=True
    with st.expander("Rediger le rapport"):
        print('yes')
        if st.button('Envoyer'):
            print('Vive IA')
            


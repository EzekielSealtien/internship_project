#!/bin/bash

# Démarrer le backend (FastAPI avec Uvicorn)
cd server
nohup uvicorn server:app --host 0.0.0.0 --port 8000 &

# Revenir à la racine du projet
cd ..

# Démarrer le frontend (Streamlit)
nohup streamlit run Client/main.py --server.port 8501 --server.address 0.0.0.0 &

import pandas as pd
import numpy as np
from skops import hub_utils
import os

"""
repo_id = "gianlab/random-forest-model-disease-symptom-prediction"
download_repo = "downloaded-model"
hub_utils.download(repo_id=repo_id, dst=download_repo)
"""

base_dir = os.path.dirname(os.path.abspath(__file__))  # Chemin absolu du script actuel
path1 = os.path.join(base_dir, 'downloaded-model', 'Symptom-severity.csv')
path2 = os.path.join(base_dir, 'downloaded-model', 'symptom_Description.csv')
path3 = os.path.join(base_dir, 'downloaded-model', 'symptom_precaution.csv')
df1 = pd.read_csv(path1)
df1['Symptom'] = df1['Symptom'].str.replace('_',' ')
discrp = pd.read_csv(path2)
ektra7at = pd.read_csv(path3)


def predd(x,a):
    psymptoms = a
    #print(psymptoms)
    a = np.array(df1["Symptom"])
    b = np.array(df1["weight"])
    for j in range(len(psymptoms)):
        found = False
        for k in range(len(a)):
            if psymptoms[j] == a[k]:
                psymptoms[j] = b[k]
                found = True
                break
        # If symptom is not found, set its value to 0
        if not found and isinstance(psymptoms[j], str):
            psymptoms[j] = 0

    psy = [psymptoms]
    pred2 = x.predict(psy)
    disp= discrp[discrp['Disease']==pred2[0]]
    disp = disp.values[0][1]
    recomnd = ektra7at[ektra7at['Disease']==pred2[0]]
    c=np.where(ektra7at['Disease']==pred2[0])[0][0]
    precuation_list=[]
    for i in range(1,len(ektra7at.iloc[c])):
          precuation_list.append(ektra7at.iloc[c,i])
    
    response={
        "disease_name":pred2[0],
        "disease_description":disp,
        "recommendations":precuation_list
    }
    return response

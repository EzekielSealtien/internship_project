import pickle
from Functions_.model import predd

path="./Functions_/downloaded-model/skops-iw9h_jza.pkl"

pickled_model=pickle.load(open(path,'rb'))

a=["stomach pain","chills","nodal skin eruptions","muscle weakness",0,0,0,0,0,0,0,0,0,0,0,0,0]
try:
    response=predd(pickled_model,a)
    if not response:
        print('Any disease')
    else:
        print(response)
except Exception as e:
    print(f" Attentionnnnnn :{str(e)}")
        
        
a=["stomach pain","chills","nodal skin eruptions","muscle weakness",0,0,0,0,0,0,0]


from flask import Flask, jsonify, request, render_template
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
filename = 'model.sav'
model_load = pickle.load(open(filename, 'rb'))


@app.route('/')
def home():
    return render_template('index.html')

standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
     if request.method == 'POST':
        CreditScore = float(request.form['CreditScore'])
        Gender= int(request.form['Gender'])        
        Tenure= int(request.form['Tenure'])
        Balance=float(request.form['Balance'])
        NumOfProducts=int(request.form['NumOfProducts'])
        HasCrCard=int(request.form['HasCrCard'])
        IsActiveMember= int(request.form['IsActiveMember'])
        EstimatedSalary= float(request.form['EstimatedSalary'])
        geo_Germany= int(request.form['geo_Germany'])
        geo_Spain= int(request.form['geo_Spain'])
        Age = int(request.form['Age']) 
        input = pd.DataFrame([[CreditScore,Gender,Tenure,Balance,NumOfProducts,HasCrCard,IsActiveMember,EstimatedSalary,geo_Germany,geo_Spain,Age]])
        output = model_load.predict(input)
        return render_template('index.html', prediction_text='Churn Output {}'.format(output))
     else:
         return render_template('index.html') 
  
    
if __name__=="__main__":
    app.run(debug=True,port=8050)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

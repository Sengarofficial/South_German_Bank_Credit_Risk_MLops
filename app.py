import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import pickle


app = Flask(__name__)

model = joblib.load('saved_models/prediction_models/xgb_clf.joblib')
scaler = pickle.load(open('saved_models/scale_models/scaling.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    if request.method == 'POST':
        age = [np.log(int(request.form['age']))]
        amount = [np.log(int(request.form['amount']))]
        credit_duration = [np.log(int(request.form['credit duration']))]
        

        status = [int(request.form['status'])]
        employment_duration  = [int(request.form['emp_dur'])]
        savings = [int(request.form['savings'])]
        other_debtors = [int(request.form['other_debtors'])]
        credit_history = [int(request.form['credit_history'])]
        purpose = [int(request.form['purpose'])]
        property = [int(request.form['property'])]
        foreign_worker = [(int(request.form['foreign_worker']))]
        personal_status_sex = [int(request.form['personal_status'])]

    features = credit_duration + amount + age + status + employment_duration + savings + other_debtors
    features = features + credit_history + purpose + property + foreign_worker + personal_status_sex

    
    features_arr = [np.array(features)]
    features_scale = scaler.transform(features_arr)

    prediction = model.predict(features_scale)
  
    result = ""
    if prediction == 1:
      result = "GOOD RISK"
    else:
      result = "BAD RISK"

    return render_template('output.html', prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True, port = 5002)

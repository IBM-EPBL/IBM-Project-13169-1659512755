from flask import Flask, render_template, request, jsonify
import numpy as np
import requests
import json

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/predictpage',methods=['POST'])
def predictpage():
    if request.method == 'POST':
        if request.form.get('action1') == 'GET STARTED':
            return render_template('predict.html')
    else:
        return render_template("homepage.html")
    # return render_template('predict.html')

@app.route('/predictpage/y_predict',methods=['POST'])
def y_predict():
        g_score= request.form["gscore"]
        t_score=request.form["tscore"]
        urs =request.form["urating"]
        sops=request.form["sop"]
        lors=request.form["lor"]
        gpa=request.form["cgpa"]
        rscore=request.form["research"]
        # deepcode ignore HardcodedNonCryptoSecret: <please specify a reason of ignoring this>
        API_KEY = "FMnFCKYFVzZjoPfxiqMInnYK2jc14D9GpJgN0mckp1wj"
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={
            "apikey": API_KEY,
            "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'
        })
        mltoken = token_response.json()["access_token"]
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

        payload_scoring = {"input_data": [
            {"field": [["GRE Score", "TOEFL Score", "University Rating", "SOP", "LOR ", "CGPA", "Research"]],
             "values": [[g_score,t_score , urs, sops, lors, gpa, rscore]]}]}

        response_scoring = requests.post(
            'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/172d4b7a-ef21-46c8-8936-2962f34ee250/predictions?version=2022-11-15',
            json=payload_scoring,
            headers={'Authorization': 'Bearer ' + mltoken})
        res = response_scoring.json()
        print(res)
        result=res['predictions'][0]['values'][0][0][0]
        coa=str(result*100)[:5]
        if result < 0.5:
            output = "Chance of admit is " + coa +" %."+ "Low chance"
        elif result >= 0.5 and result < 0.65:
            output = "Chance of admit is " + coa +" %."+  "Moderate chance"
        elif result >= 0.65 and result < 0.8:
            output = "Chance of admit is " + coa +" %."+  "Good chance"
        elif result >= 0.8 and result <= 1.0:
            output = "Chance of admit is " + coa +" %."+  "High chance"
        return render_template('Result.html',prediction_text=output)

@app.route('/predictpage/y_predict/redirectpage',methods=['POST'])
def redirectpage():
    if request.method == 'POST':
        if request.form.get('action1') == 'Retry':
            return render_template('predict.html')
    else:
        return render_template("homepage.html")

if __name__ == "__main__":
    app.debug=True
    app.run()
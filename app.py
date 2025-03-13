from flask import Flask, render_template, redirect, url_for, request, flash
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.pred_pipeline import input_data, Pred_Pipeline

app = Flask(__name__)
# app.secret_key = 'your_secret_key_here'  # Change this to a secure random key in production


# Route for home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for about page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route for legal page
@app.route('/legal')
def legal():
    return render_template('legal.html')

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login form submission here
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Basic validation
        if not email or not password:
            flash('Please enter both email and password', 'error')
        else:
            # For demonstration purposes - in a real app, you would validate against a database
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
    
    return render_template('login.html')

# Route for signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle signup form submission here
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Basic validation
        if not email or not password:
            flash('Please enter both email and password', 'error')
        else:
            # For demonstration purposes - in a real app, you would save to a database
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('signup.html')

# Route for makepred page
@app.route('/makepredictions')
def makepredictions():
    return render_template('makepredictions.html')

# Route for results page
@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('results.html')
    else:
        data = input_data(
            Age=int(request.form.get('Age', 0)),
            Income=float(request.form.get('Income', 0.0)),
            Home=request.form.get('Home', ''),
            Emp_length=float(request.form.get('Emp_length', 0.0)),
            Intent=request.form.get('Intent', ''),
            Amount=float(request.form.get('Amount', 0.0)),
            Rate=float(request.form.get('Rate', 0.0)),
            Status=request.form.get('Status', ''),
            Percent_income=float(request.form.get('Percent_income', 0.0)),
            Cred_length=int(request.form.get('Cred_length', 0))
        )
        pred_data = data.transfrom_data_as_dataframe()
        print(pred_data)
        print("Before Prediction")

        predict_pipeline = Pred_Pipeline()
        print("During Prediction")
        results, probability, message = predict_pipeline.predict(pred_data)
        print("After Prediction")
        
        # Use the message directly from the prediction pipeline
        return render_template('results.html', results=message)

# Custom 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Serve component HTML files
@app.route('/components/<component_name>')
def serve_component(component_name):
    return render_template(f'components/{component_name}')

if __name__ == '__main__':
    app.run(debug=True) 
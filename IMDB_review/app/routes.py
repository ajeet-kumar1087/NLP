from flask import Flask, request, redirect, url_for, jsonify,render_template

from app import application

import pandas as pd
import mysql.connector
from mysql.connector import Error
from app.service import Service

@application.route('/')
def welcome():
    return 'welcome to the web app'


@application.route('/fetch-add', methods=['GET', 'POST'])
def add_review():
    #insert_reviews()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM reviews")
        reviews = [
            dict(id = row[0], review = row[1], label = row[2])
            for row in cursor.fetchall()  
        ]

        if reviews is not None:
            return jsonify((reviews))

    if request.method == 'POST':
        nw_text = request.form['text']
        nw_label = request.form['label']
        response = Service.persist_data(nw_text, nw_label)
        return response

@application.route('/single-review', methods = ['GET'])
def fetchOne():
    review =  Service.fetch_latest_review()
    print("workin")
    return jsonify(review)

@application.route('/success/<label>')
def success(label):
    if(label == '0'):
        label_ = 'Negative'
    else:
        label_ = 'Positive'
    return render_template('result.html', label = label_)

@application.route('/predict', methods=['POST','GET'])
def load_predict():
    if request.method == 'POST':
        nw_text = request.form["review"]
        nw_label = Service.load_and_predict(nw_text)
        return redirect(url_for('success', label = nw_label))
    return render_template("feedback.html")
    
@application.route('/train-predict', methods = ['GET', 'POST'])
def train_predict():
    print('train-predict route')
    if request.method == 'POST':
        nw_text = request.form["review"]
        nw_label = Service.train_and_predict(nw_text)
        return redirect(url_for('success', label = nw_label))
    return render_template("train-predict.html")

    
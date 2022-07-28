from flask import Flask, request, redirect, url_for, jsonify

import copy
from app.predict import Predict
from app.preprocess import DataPreprocessing
import pandas as pd
import mysql.connector
from mysql.connector import Error
from app.sql_connect import DataBase
import pymysql
from app import predict

class Service:

    def insert_reviews():
        # Insert DataFrame to Table
        data = pd.read_csv (r'C:\Users\91895\Desktop\NLP\dataset\Test.csv')   
        df = pd.DataFrame(data)
        conn = DataBase.db_connection()
        cursor = conn.cursor()
        for i,row in df.iterrows():
            cursor.execute("""
                    INSERT INTO reviews ( Review, Label)
                    VALUES (%s,%s)
                    """, 
                    tuple(row)
                    )
        conn.commit()

        
    def persist_data(text, label):
        conn = DataBase.db_connection()
        cursor = conn.cursor()
        sql = """INSERT INTO reviews (Review, Label)
                VALUES(%s,%s)"""
        value  =(text, label)
        cursor.execute(sql,value)
        conn.commit()
        return f"Book with the id: {cursor.lastrowid} created succesfully"

    def load_and_predict(text):
        print('load predict method')
        text_persist = text
        dp = DataPreprocessing()
        preprocessed_text = dp.apply_all( text)
        pred = Predict()
        X = predict.load_word_to_tf_idf([text])
        label = pred.load_predict( X)

        #inserting text and predicted data into the table
        conn = DataBase.db_connection()
        cursor = conn.cursor()
        sql = """INSERT INTO reviews (Review, Label)
                    VALUES(%s,%s)"""
        value  =(text_persist, int(label[0]))
        cursor.execute(sql,value)
        conn.commit()
        return int(label[0])
    
    
    def train_and_predict(text):
        print('print train predict method')
        pred = Predict()
        X,y = predict.create_word_to_tf_idf()
        pred.train_model(X,y)
        print('train successfull')
        text_persist = text
        dp = DataPreprocessing()
        preprocessed_text = dp.apply_all( text)

        tfidf_vec = pred.loadTransform_tf_idf([preprocessed_text])
        label = pred.load_predict( tfidf_vec)
        print('prediction successful')

        #inserting text and predicted data into the table
        conn = DataBase.db_connection()
        cursor = conn.cursor()
        sql = """INSERT INTO reviews (Review, Label)
                    VALUES(%s,%s)"""
        value  =(text_persist, int(label[0]))
        cursor.execute(sql,value)
        conn.commit()
        return int(label[0])


    def fetch_latest_review():
        conn = DataBase.db_connection()
        cursor = conn.cursor()
        print('working')
        sql = """ SELECT * FROM reviews ORDER BY ID DESC LIMIT 1 """
        cursor.execute(sql)

        reviews = [
            dict(id = row[0], review = row[1], label = row[2])
            for row in cursor.fetchall()
        ]
        if reviews is not None:
            return reviews
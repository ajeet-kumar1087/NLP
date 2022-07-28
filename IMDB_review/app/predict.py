
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from xgboost import XGBClassifier
import pickle
import os
from app.preprocess import DataPreprocessing
from app.sql_connect import DataBase
import pymysql
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

class Predict:
    def __init__(self ):
        # self.text = text
        self.data_preprocess = DataPreprocessing()

    def createTransform_tf_idf(self, text):
        print('writing tf_idf pickle file')
        tfidf = TfidfVectorizer(strip_accents = None, lowercase = False, preprocessor = None,  use_idf = True, norm = 'l2', smooth_idf = True)
        X = tfidf.fit_transform(text)
        pickle.dump(tfidf, open(r"app\pickle\tf_idf.pickle" , "wb"))
        print(X.shape)
        return X


    def loadTransform_tf_idf(self, text):
        print('load tf_idf function')
        tf_idf = pickle.load(open(r"app\pickle\tf_idf.pickle" , "rb"))
        X = tf_idf.transform(text)
        return X

    def train_model(self, X, y):
        xgb = XGBClassifier()
        xgb.fit(X,y)
        print('train successful')
        pickle.dump(xgb, open(r"app\pickle\xgb.pickle", "wb"))
        

    def load_predict(self, X):
        xgb = pickle.load(open(r"app\pickle\xgb.pickle", "rb"))
        y = xgb.predict(X)
        return y

def word_to_tf_idf():
    conn = DataBase.db_connection()
    data = pd.read_sql("select Review, Label from reviews LIMIT 1000", conn)
    data.rename(columns = {'Review': 'text', 'Label':'label'}, inplace = True)
    dataPre = DataPreprocessing()
    data['text'] = data['text'].apply(lambda x: dataPre.apply_all(x))
    y = data['label']
    print(data['text'][10])
    predict = Predict()
    tf_idf = predict.createTransform_tf_idf(data['text'])
    print(tf_idf.shape)
    return (tf_idf , y)







    


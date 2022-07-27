import mysql.connector
from mysql.connector import Error

class DataBase:
    def connect_db():
        
        try:
            connection = mysql.connector.connect(host='localhost',
                                                
                                                database='IMDB',
                                                user='root',
                                                password='12345678')

            mySql_Create_Table_Query = """CREATE TABLE IF NOT EXIST Reviews ( 
                                    Id int NOT NULL AUTO_INCREMENT,
                                    Review text(250000) NOT NULL,
                                    Label int,
                                    PRIMARY KEY (Id)) """

            # alter_query = """ALTER TABLE Reviews
            # CHANGE COLUMN Review Review text(250000) NOT NULL """
            cursor = connection.cursor()
            result = cursor.execute(mySql_Create_Table_Query)
            # res = cursor.execute(alter_query)
            print("Reviews Table created successfully ")

        except mysql.connector.Error as error:
            print("Failed to create table in MySQL: {}".format(error))
        # finally:
        #     if connection.is_connected():
        #         cursor.close()
        #         connection.close()
        #         print("MySQL connection is closed")

    def db_connection():
        connection = None
        try: 
            connection = mysql.connector.connect(host='localhost',
                                            database='IMDB',
                                            user='root',
                                            password='12345678')
        except Error as e:
            print("Error while connecting to MySQL", e)
        
        return connection

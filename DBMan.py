import mysql.connector

class DataBase:
    db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'password',
    database = 'trucks'
    )
    cursor = mydb.cursor()

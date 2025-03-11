import pymysql
import random
 
db = pymysql.connect(host='localhost',user='root',password='boom99xd')
 
cursor = db.cursor()
 
# Instrucción SQL QUERY
sql = "CREATE DATABASE IF NOT EXISTS USERS_IET701"
cursor.execute(sql)

sql2 = "USE USERS_IET701"
cursor.execute(sql2)
 
sql3 = '''CREATE Table if not exists Sensor1(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        Temperatura FLOAT NOT NULL, Humedad FLOAT NOT NULL)'''
       
cursor.execute(sql3)

temp = random.uniform(-20,200)
hum = random.uniform(0,100)

for i in range(100):
    temp = random.uniform(-20,200)
    hum = random.uniform(0,100)
    sql4 = "INSERT INTO Sensor1(Temperatura,Humedad) VALUES (%s,%s)"
    cursor.execute(sql4,(temp,hum))
    db.commit()

db.close()
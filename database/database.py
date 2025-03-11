import pymysql
 
db = pymysql.connect(host='localhost',user='root',password='boom99xd')
 
cursor = db.cursor()
 
# Instrucción SQL QUERY
sql = "CREATE DATABASE IF NOT EXISTS proyecto2"
cursor.execute(sql)
 
sql2 = "USE proyecto2"
cursor.execute(sql2)
 
sql3 = '''CREATE Table if not exists Zona5(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, Temperatura FLOAT, CO2 FLOAT, Presion FLOAT,timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)'''
       
cursor.execute(sql3)
 
#sql4 = '''INSERT INTO Users(Usuario,Password) VALUES("Alan47","test123")'''
#sql5 = '''INSERT INTO Users(Usuario,Password) VALUES("David55","test12")'''
#sql6 = '''INSERT INTO Users(Usuario,Password) VALUES("Alan4","test1")'''
#sql7 = '''INSERT INTO Users(Usuario,Password) VALUES("Jose7","test23")'''
#sql8 = '''INSERT INTO Users(Usuario,Password) VALUES("Ana77","test1234")'''
 
#cursor.execute(sql4)
#cursor.execute(sql5)
#cursor.execute(sql6)
#cursor.execute(sql7)
#cursor.execute(sql8)
 
#db.commit()
 
#sql9 = "SELECT * FROM Users"
 
#cursor.execute(sql9)
 
#datos = cursor.fetchall()
 
#for dato in datos:
#    print(f"Valor de tabla es: {dato}")
 
db.close()
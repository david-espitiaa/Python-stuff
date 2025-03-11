import paho.mqtt.client as mqtt
import random
import pymysql
import time
from PyQt5 import QtWidgets, uic, QtCore
import pyqtgraph as pg
import json

timer = QtCore.QTimer()
timer.setInterval(5000)

app = QtWidgets.QApplication([])
gui = uic.loadUi('mainProyecto2.ui')
gui2 = uic.loadUi('tabla.ui')

sensor_1 = False
temp_1 = None
co2_1 = None
pA_1 = None

sensor_2 = False
temp_2 = None
co2_2 = None
pA_2 = None

sensor_3 = False
temp_3 = None
co2_3 = None
pA_3 = None

sensor_4 = False
temp_4 = None
co2_4 = None
pA_4 = None

sensor_5 = False
temp_5 = None
co2_5 = None
pA_5 = None


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conexión exitosa")
    else:
        print(f"Error de conexión, código: {rc}")

broker = "bc3e2035e36f4fcaa9f55d48bbe8f2a7.s1.eu.hivemq.cloud"
port = 8883  # Usar puerto seguro
topic = "sensores/data"
# Configuración del cliente MQTT
cliente = mqtt.Client()
# Configurar credenciales
usuario = "david99"  # Sustituye con tu nombre de usuario de HiveMQ Cloud
contraseña = "Holadavid9"  # Sustituye con tu contraseña de HiveMQ Cloud
cliente.username_pw_set(usuario, contraseña)
# Habilitar TLS/SSL para HiveMQ
cliente.tls_set()  # Configura automáticamente los certificados TLS predeterminados
# Definir la función de callback cuando se conecta
cliente.on_connect = on_connect
# Conectar al broker con TLS/SSL
print("Conectando al broker...")
cliente.connect(broker, port, keepalive=60)
# Iniciar el bucle de la red para gestionar la conexión y callbacks
cliente.loop_start()




def s1True():
    global sensor_1
    sensor_1 = True

def s1False():
    global sensor_1
    sensor_1 = False

def s2True():
    global sensor_2
    sensor_2 = True

def s2False():
    global sensor_2
    sensor_2 = False

def s3True():
    global sensor_3
    sensor_3 = True

def s3False():
    global sensor_3
    sensor_3 = False

def s4True():
    global sensor_4
    sensor_4 = True

def s4False():
    global sensor_4
    sensor_4 = False

def s5True():
    global sensor_5
    sensor_5 = True

def s5False():
    global sensor_5
    sensor_5 = False

def printv():
    global temp_1
    global co2_1
    global pA_1
    global sensor_1
    print(sensor_1)
    print(temp_1)
    print(co2_1)
    print(pA_1)

def exit():
    gui2.destroy()
    gui.show()

def update():
    global temp_1
    global co2_1
    global pA_1
    global sensor_1
    global temp_2
    global co2_2
    global pA_2
    global sensor_2
    global temp_3
    global co2_3
    global pA_3
    global sensor_3
    global temp_4
    global co2_4
    global pA_4
    global sensor_4
    global temp_5
    global co2_5
    global pA_5
    global sensor_5

    if sensor_1 == True:
        temp_1 = round(random.uniform(20.0, 50.0), 2)
        co2_1 = round(random.uniform(400.0, 1000.0), 2)
        pA_1 = round(random.uniform(900.0, 1100.0), 2)    
    else:
        temp_1 = None
        co2_1 = None
        pA_1 = None

    if sensor_2 == True:
        temp_2 = round(random.uniform(20.0, 50.0), 2)
        co2_2 = round(random.uniform(400.0, 1000.0), 2)
        pA_2 = round(random.uniform(900.0, 1100.0), 2)      
    else:
        temp_2 = None
        co2_2 = None
        pA_2 = None
    
    if sensor_3 == True:
        temp_3 = round(random.uniform(20.0, 50.0), 2)
        co2_3 = round(random.uniform(400.0, 1000.0), 2)
        pA_3 = round(random.uniform(900.0, 1100.0), 2)     
    else:
        temp_3 = None
        co2_3 = None
        pA_3 = None
    
    if sensor_4 == True:
        temp_4 = round(random.uniform(20.0, 50.0), 2)
        co2_4 = round(random.uniform(400.0, 1000.0), 2)
        pA_4 = round(random.uniform(900.0, 1100.0), 2)      
    else:
        temp_4 = None
        co2_4 = None
        pA_4 = None
    
    if sensor_5 == True:
        temp_5 = round(random.uniform(20.0, 50.0), 2)
        co2_5 = round(random.uniform(400.0, 1000.0), 2)
        pA_5 = round(random.uniform(900.0, 1100.0), 2)     
    else:
        temp_5 = None
        co2_5 = None
        pA_5 = None


    datos_sensor = {
        "Temperatura1": temp_1,
        "CO21": co2_1,
        "Presion1": pA_1,
        "Temperatura2": temp_2,
        "CO22": co2_2,
        "Presion2": pA_2,
        "Temperatura3": temp_3,
        "CO23": co2_3,
        "Presion3": pA_3,
        "Temperatura4": temp_4,
        "CO24": co2_4,
        "Presion4": pA_4,
        "Temperatura5": temp_5,
        "CO25": co2_5,
        "Presion5": pA_5,
    }
    # Publicar los datos en formato JSON
    cliente.publish(topic, json.dumps(datos_sensor))
    print(f"Datos enviados: {datos_sensor}")

def visualizar_tabla1():
    gui.hide()
    gui2.show()
    try:
        #Verificamos la conexión a la DB
        db = pymysql.connect(host='localhost',user='root',password='boom99xd',database='proyecto2')
       
        cursor = db.cursor()
       
        sql = "SELECT * FROM zona1"
       
        cursor.execute(sql)
       
        tabla = cursor.fetchall()
       
        gui2.tabla.setRowCount(0)
 
        for no_fila, dato_fila in enumerate(tabla):
            gui2.tabla.insertRow(no_fila)
            for no_columna, dato in enumerate(dato_fila):
                dato = QtWidgets.QTableWidgetItem(str(dato))
                gui2.tabla.setItem(no_fila,no_columna,dato)
       
        db.close()
    except Exception as e:
        print(e)
def visualizar_tabla2():
    gui.hide()
    gui2.show()
    try:
        #Verificamos la conexión a la DB
        db = pymysql.connect(host='localhost',user='root',password='boom99xd',database='proyecto2')
       
        cursor = db.cursor()
       
        sql = "SELECT * FROM zona2"
       
        cursor.execute(sql)
       
        tabla = cursor.fetchall()
       
        gui2.tabla.setRowCount(0)
 
        for no_fila, dato_fila in enumerate(tabla):
            gui2.tabla.insertRow(no_fila)
            for no_columna, dato in enumerate(dato_fila):
                dato = QtWidgets.QTableWidgetItem(str(dato))
                gui2.tabla.setItem(no_fila,no_columna,dato)
       
        db.close()
    except Exception as e:
        print(e)
def visualizar_tabla3():
    gui.hide()
    gui2.show()
    try:
        #Verificamos la conexión a la DB
        db = pymysql.connect(host='localhost',user='root',password='boom99xd',database='proyecto2')
       
        cursor = db.cursor()
       
        sql = "SELECT * FROM zona3"
       
        cursor.execute(sql)
       
        tabla = cursor.fetchall()
       
        gui2.tabla.setRowCount(0)
 
        for no_fila, dato_fila in enumerate(tabla):
            gui2.tabla.insertRow(no_fila)
            for no_columna, dato in enumerate(dato_fila):
                dato = QtWidgets.QTableWidgetItem(str(dato))
                gui2.tabla.setItem(no_fila,no_columna,dato)
       
        db.close()
    except Exception as e:
        print(e)
def visualizar_tabla4():
    gui.hide()
    gui2.show()
    try:
        #Verificamos la conexión a la DB
        db = pymysql.connect(host='localhost',user='root',password='boom99xd',database='proyecto2')
       
        cursor = db.cursor()
       
        sql = "SELECT * FROM zona4"
       
        cursor.execute(sql)
       
        tabla = cursor.fetchall()
       
        gui2.tabla.setRowCount(0)
 
        for no_fila, dato_fila in enumerate(tabla):
            gui2.tabla.insertRow(no_fila)
            for no_columna, dato in enumerate(dato_fila):
                dato = QtWidgets.QTableWidgetItem(str(dato))
                gui2.tabla.setItem(no_fila,no_columna,dato)
       
        db.close()
    except Exception as e:
        print(e)
def visualizar_tabla5():
    gui.hide()
    gui2.show()
    try:
        #Verificamos la conexión a la DB
        db = pymysql.connect(host='localhost',user='root',password='boom99xd',database='proyecto2')
       
        cursor = db.cursor()
       
        sql = "SELECT * FROM zona5"
       
        cursor.execute(sql)
       
        tabla = cursor.fetchall()
       
        gui2.tabla.setRowCount(0)
 
        for no_fila, dato_fila in enumerate(tabla):
            gui2.tabla.insertRow(no_fila)
            for no_columna, dato in enumerate(dato_fila):
                dato = QtWidgets.QTableWidgetItem(str(dato))
                gui2.tabla.setItem(no_fila,no_columna,dato)
       
        db.close()
    except Exception as e:
        print(e)

gui.btnA1.clicked.connect(s1True)
gui.btnD1.clicked.connect(s1False)
gui.btnT1.clicked.connect(visualizar_tabla1)
gui.btnA2.clicked.connect(s2True)
gui.btnD2.clicked.connect(s2False)
gui.btnT2.clicked.connect(visualizar_tabla2)
gui.btnA3.clicked.connect(s3True)
gui.btnD3.clicked.connect(s3False)
gui.btnT3.clicked.connect(visualizar_tabla3)
gui.btnA4.clicked.connect(s4True)
gui.btnD4.clicked.connect(s4False)
gui.btnT4.clicked.connect(visualizar_tabla4)
gui.btnA5.clicked.connect(s5True)
gui.btnD5.clicked.connect(s5False)
gui.btnT5.clicked.connect(visualizar_tabla5)
gui2.btnExit.clicked.connect(exit)


timer.timeout.connect(update)
timer.start()

gui.show()
app.exec()


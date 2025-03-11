import paho.mqtt.client as mqtt
import random
import time
import json 
broker = "localhost"
topic = "sensor/data"
port = 1883
cliente = mqtt.Client()
cliente.connect(broker, port)

def valoresSensor():
    while True:
        temp = round(random.uniform(20.0,30.0),2)
        hum = round(random.uniform(20.0,70.0),2)
        datos_sensor = {"Temperatura": temp, "Humedad": hum}
        cliente.publish(topic, json.dumps(datos_sensor))
        time.sleep(10)

if __name__ == "__main__":
    valoresSensor()



    


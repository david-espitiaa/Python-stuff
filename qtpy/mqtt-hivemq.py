import paho.mqtt.client as mqtt
import random
import time
import json


# Función de callback en caso de conexión exitosa
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conexión exitosa")
    else:
        print(f"Error de conexión, código: {rc}")


# Función para enviar valores del sensor simulados
def valores_sensor():
    broker = "bc3e2035e36f4fcaa9f55d48bbe8f2a7.s1.eu.hivemq.cloud"
    port = 8883  # Usar puerto seguro
    topic = "sensor/data"


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


    # Enviar valores del sensor
    while True:
        #temp = round(random.uniform(20.0, 50.0), 2)
        temp = None
        hum = None
        temp2 = round(random.uniform(20.0, 50.0), 2)
        hum2 = round(random.uniform(20.0, 70.0), 2)
        temp3 = round(random.uniform(20.0, 50.0), 2)
        hum3 = round(random.uniform(20.0, 70.0), 2)
        datos_sensor = {
            "Temperatura": temp,
            "Humedad": hum,
            "Temperatura2": temp2,
            "Humedad2": hum2,
            "Temperatura3": temp3,
            "Humedad3": hum3,
        }
        # Publicar los datos en formato JSON
        cliente.publish(topic, json.dumps(datos_sensor))
        print(f"Datos enviados: {datos_sensor}")
        time.sleep(5)


if __name__ == "__main__":
    valores_sensor()
import paho.mqtt.client as mqtt
import base64
from io import BytesIO
from PIL import Image

# Configuración del broker MQTT
broker = "bc3e2035e36f4fcaa9f55d48bbe8f2a7.s1.eu.hivemq.cloud"
port = 8884
topic = "esp32cam/foto"  # Tópico que usas para recibir la imagen

# Función que se ejecuta cuando se recibe un mensaje del broker MQTT
def on_message(client, userdata, message):
    print("Imagen recibida. Decodificando...")

    # Decodificar la imagen base64
    image_base64 = message.payload.decode("utf-8")
    image_data = base64.b64decode(image_base64)

    # Convertir los bytes en una imagen
    image = Image.open(BytesIO(image_data))

    # Mostrar la imagen
    image.show()

# Función que se ejecuta cuando el cliente MQTT se conecta al broker
def on_connect(client, userdata, flags, rc):
    print("Conectado a MQTT con código de resultado: " + str(rc))
    # Suscribirse al tópico
    client.subscribe(topic)

# Crear instancia del cliente MQTT
client = mqtt.Client()

# Asignar funciones de manejo de eventos
client.on_connect = on_connect
client.on_message = on_message

# Conectar al broker MQTT
client.connect(broker, port, 60)

# Iniciar el loop de MQTT para escuchar mensajes
client.loop_forever()

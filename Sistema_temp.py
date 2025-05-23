import time
import random
from machine import Pin
from umqtt_simple import MQTTClient

# Configuración del broker
mqtt_broker = "192.168.80.49"
client_id = "picoW_simulator"
topic_base = b"temperatura/sensor"
topic_control_base = b"resistencia/control/"

# Crear 5 pines para las resistencias (usa los GPIOs disponibles)
resistencias = {
    "1": Pin(15, Pin.OUT),
    "2": Pin(14, Pin.OUT),
    "3": Pin(13, Pin.OUT),
    "4": Pin(12, Pin.OUT),
    "5": Pin(11, Pin.OUT)
}

# Función para manejar los mensajes recibidos
def manejar_mensaje(topic, msg):
    topic_str = topic.decode()
    print(f"Mensaje recibido: {topic_str} → {msg} (raw bytes: {msg})")

    if topic_str.startswith("resistencia/control/"):
        num = topic_str.split("/")[-1]
        if num in resistencias:
            try:
                valor = int(msg)  # Convertir bytes a int
            except ValueError:
                print(f"Error: mensaje no es un entero válido: {msg}")
                return

            if valor == 1:
                resistencias[num].value(1)
                print(f"Resistencia {num} ENCENDIDA")
            elif valor == 0:
                resistencias[num].value(0)
                print(f"Resistencia {num} APAGADA")
            else:
                print(f"Valor no esperado para resistencia {num}: {valor}")

# Inicializar MQTT
client = MQTTClient(client_id, mqtt_broker)
client.set_callback(manejar_mensaje)
client.connect()
print("Conectado al broker MQTT")

# Suscribirse a los 5 topics de control
for i in range(1, 6):
    topic = topic_control_base + str(i).encode()
    client.subscribe(topic)
    print(f"Suscrito a {topic.decode()}")

# Simular temperatura entre 15 y 35 °C
def simular_temperatura():
    return round(random.uniform(15.0, 35.0), 2)

try:
    while True:
        # Publicar temperatura simulada
        for i in range(1, 6):
            temp = simular_temperatura()
            topic = topic_base + str(i).encode()
            payload = str(temp)
            client.publish(topic, payload)
            print(f"Enviado {payload} °C a {topic.decode()}")
        
        # Revisar si hay comandos de control
        for _ in range(10):
            client.check_msg()
            time.sleep(0.5)

except KeyboardInterrupt:
    print("Detenido por el usuario")

finally:
    try:
        client.disconnect()
        print("MQTT desconectado")
    except:
        print("Error al cerrar la conexión MQTT")
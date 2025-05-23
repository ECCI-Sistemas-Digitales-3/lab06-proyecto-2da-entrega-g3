import network
import time

ssid = 'Infinix NOTE 40'
password = 'H4ru3245'

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando a la red WiFi...')
        wlan.connect(ssid, password)
        timeout = 10  # segundos
        inicio = time.time()
        while not wlan.isconnected():
            if time.time() - inicio > timeout:
                print("No se pudo conectar al WiFi.")
                return
            time.sleep(1)
    print('Conectado. IP:', wlan.ifconfig()[0])

conectar_wifi()
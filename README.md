[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=19409481&assignment_repo_type=AssignmentRepo)
# Lab06: Proyecto 2da. entrega

## Integrantes
[Julieth Alejandra Sandoval Estupiñan](https://github.com/Julieth-Sandoval)

[Jose Angel Campo Vargas](https://github.com/Jose-Angel-Campo-Vargas)

[David Leonardo Castaño Madrigal](https://github.com/IngleonardocM)

## Documentación
# Sistema de Control de Temperatura con MQTT para Calentamiento de Pintura

Este proyecto implementa un sistema distribuido que comunica una **Raspberry Pi Pico W** con una **Raspberry Pi Zero 2W** a través del protocolo **MQTT**, con el objetivo de **medir y controlar la temperatura** de un conjunto de resistencias que calientan pintura para reducir su viscosidad. La Raspberry Pi Zero 2W también ejecuta un entorno de **Node-RED** para tomar decisiones automatizadaz y dar la visualización de los datos.

---

## 🧩 Arquitectura del Sistema

- **📡 Raspberry Pi Pico W**  
  - Simula la lectura de **5 sensores DS18B20**.
  - Publica las temperaturas vía MQTT.
  - Recibe órdenes de encendido/apagado de resistencias desde Node-RED.
  - Ejecuta el script [`Sistema_temp.py`](./Sistema_temp.py).

- **💻 Raspberry Pi Zero 2W**  
  - Ejecuta **Node-RED**.
  - Suscribe las temperaturas publicadas por la Pico W.
  - Controla cuándo encender o apagar cada resistencia (según límite de 30°C).
  - Entrega la visualización del sistema.
  - Flujo completo disponible en [`ControlTemp.json`](./ControlTemp.json).

---

## ⚙️ Archivos principales

### 🔧 `Sistema_temp.py`

Este script corre en la **Raspberry Pi Pico W** y tiene las siguientes funciones:

### Monitoreo de Temperatura
El sistema lee datos de 5 sensores de temperatura independientes:
- `temperatura/sensor1`
- `temperatura/sensor2`
- `temperatura/sensor3`
- `temperatura/sensor4`
- `temperatura/sensor5`

### Control de Resistencias
El sistema permite el control de 5 resistencias mediante suscripción a topics MQTT:
- `resistencia/control/1`
- `resistencia/control/2`
- `resistencia/control/3`
- `resistencia/control/4`
- `resistencia/control/5`

**Publicación de temperatura simulada** entre 15°C y 35°C en los tópicos:

- **Encendido o apagado** de resistencias mediante pines GPIO si se recibe un `1` (encender) o `0` (apagar) desde Node-RED.

📄 Ver archivo: [`Sistema_temp.py`](./Sistema_temp.py)

> ⚠️ Nota: Las temperaturas son **simuladas** con valores aleatorios porque no se contaba con los cinco sensores reales. El código está diseñado para integrarlos fácilmente reemplazando la función `simular_temperatura()` con lecturas reales usando `ds18x20.py` y `onewire.py`.

---

### 🔗 Librerías utilizadas en MicroPython

- `ds18x20.py` – para manejar sensores DS18B20.
- `onewire.py` – protocolo 1-Wire para los sensores.
- `umqtt_simple.py` – cliente MQTT ligero.
- `WiFi.py` – configuración de conexión WiFi.

---

## 🧠 Lógica de Control en Node-RED

El archivo [`ControlTemp.json`](./ControlTemp.json) contiene el flujo completo de Node-RED. Lo que hace es:

1. **Escuchar** los mensajes en los tópicos `temperatura/sensorX`.
2. Mostrar cada temperatura en:
 - Medidores (`gauge`)
 - Indicadores LED (`LED`)
 - Texto (`text`)
 - Gráfica histórica (`chart`)
3. Verificar si la temperatura es menor a **30°C**:
 - Si es menor: envía un **`1`** al tópico `resistencia/control/X`.
 - Si es mayor o igual: envía un **`0`**.

Esto mantiene cada resistencia funcionando dentro del rango deseado.

📄 Ver archivo: [`ControlTemp.json`](./ControlTemp.json)

---

## 📲 Requisitos

- Raspberry Pi Pico W con MicroPython instalado.
- Raspberry Pi Zero 2W con Node-RED instalado.
- Broker MQTT accesible en la red local (por defecto usa `192.168.80.49`).
- Ambos dispositivos deben estar en la **misma red WiFi**.

---

## 🚀 Cómo iniciar

### En la Raspberry Pi Pico W:
1. Sube el archivo `Sistema_temp.py` y las librerías necesarias a la placa.
2. Asegúrate de tener configurada la conexión WiFi.
3. Ejecuta el script.

### En la Raspberry Pi Zero 2W:
1. Abre Node-RED (`http://localhost:1880`).
2. Importa el archivo [`ControlTemp.json`](./ControlTemp.json).
3. Conecta el flujo y despliega el dashboard (`http://localhost:1880/ui`).

---

## 📈 Resultados esperados

- Las temperaturas simuladas deben visualizarse en el dashboard.
- Las resistencias se activan solo si la temperatura está por debajo del umbral (30°C).
- El usuario puede observar el estado y comportamiento del sistema en tiempo real.

---

## ✅ Mejoras futuras

- Integración con sensores reales DS18B20.
- Control PID para regular temperatura más preciso.
- Alarmas por sobrecalentamiento.
- Almacenamiento de datos históricos en base de datos.

---

## 🖼️ Visualizaciones del Sistema

A continuación se presentan capturas del flujo en Node-RED y del dashboard utilizado para la visualización y control de las temperaturas:

### 🔄 Flujo en Node-RED

El siguiente diagrama muestra cómo Node-RED gestiona los mensajes MQTT provenientes de cada sensor, toma decisiones de control según la temperatura (umbral de 30°C) y envía comandos de encendido o apagado a las resistencias correspondientes:

![Flujo Node-RED parte 1](/IMAGENES/flujo1.png)
![Flujo Node-RED parte 2](/IMAGENES/flujo2.png)

### 📊 Dashboard de Visualización

El dashboard web generado en Node-RED permite visualizar en tiempo real las temperaturas de los sensores, el estado de cada resistencia y gráficas históricas por cada sensor. También incluye indicadores visuales tipo LED para cada resistencia:

![Dashboard Node-RED 1](/IMAGENES/Dashboard1.png)
![Dashboard Node-RED 2](/IMAGENES/Dashboard2.png)
---


import socket
import time
import threading
import csv

# Configuración del servidor (gateway)
SERVER_IP = "127.0.0.1"
SERVER_PORT = 8001

# Ruta al CSV con los datos de sensores
CSV_FILE = "clima.csv"

# Definición de sensores disponibles (key -> columna CSV)
SENSORES = {
    1: ("TEMP", "Temperature (C)"),
    2: ("APAR", "Apparent Temperature (C)"),
    3: ("HUMI", "Humidity"),
    4: ("WIND", "Wind Speed (km/h)"),
    5: ("PRES", "Pressure (millibars)")
}

# Cargar datos del CSV
def cargar_datos():
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

DATOS = cargar_datos()


def sensor_client(key, nombre_columna, intervalo=2):
    """Hilo que simula un sensor enviando datos cada cierto tiempo"""
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_IP, SERVER_PORT))
        print(f"[+] Sensor {key} conectado al gateway")

        i = 0
        while True:
            fila = DATOS[i % len(DATOS)]   # recorrer el CSV en bucle
            valor = fila[nombre_columna]
            timestamp = fila["Formatted Date"]

            # Mensaje: KEY,valor,timestamp
            msg = f"{key},{valor},{timestamp}"
            print(f"[{key}] Enviando: {msg}")
            client.send(msg.encode("utf-8")[:1024])

            try:
                response = client.recv(1024).decode("utf-8")
                if response.lower() == "closed":
                    break
                print(f"[{key}] Respuesta del gateway: {response}")
            except:
                pass

            time.sleep(intervalo)
            i += 1

    except Exception as e:
        print(f"[!] Error en sensor {key}: {e}")
    finally:
        client.close()
        print(f"[x] Sensor {key} desconectado")


def run_clients():
    print("=== Sensores disponibles ===")
    for i, (key, nombre) in SENSORES.items():
        print(f"{i}. {key} -> {nombre}")

    seleccion = input("Seleccione sensores (ej: 1,3,4): ")
    indices = [int(x.strip()) for x in seleccion.split(",") if x.strip().isdigit()]

    for idx in indices:
        if idx in SENSORES:
            key, columna = SENSORES[idx]
            hilo = threading.Thread(target=sensor_client, args=(key, columna, 5))
            hilo.daemon = True
            hilo.start()
            print(f"✔️ Hilo para sensor {key} ({columna}) iniciado.")
        else:
            print(f"⚠️ Sensor {idx} no existe.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDeteniendo sensores...")


if __name__ == "__main__":
    print("Iniciando simulador de sensores con timestamp del CSV...")
    run_clients()

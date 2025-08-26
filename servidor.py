import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garden_pip.settings')
django.setup()

import sqlite3
import socket
import time
import threading
import json

from core.alert_engine import check_for_alerts
from main_menu.models import Alerta

CONFIG_FILE_PATH = "main_menu/config/config.json"


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        return conn
    except sqlite3.Error as e:
        print(f"Error en conexión: {e}")
        return None


def insertar_datos(conn, sensor_code, valor, timestamp):
    try:
        cursor = conn.cursor()
        consulta = "INSERT INTO main_menu_sensordata (sensor_type, value, timestamp) VALUES (?, ?, ?)"
        cursor.execute(consulta, (sensor_code, valor, timestamp))
        conn.commit()
        print(f"✓ Insertado: sensor={sensor_code}, valor={valor}, timestamp={timestamp}")
    except sqlite3.Error as e:
        print(f"Error al insertar datos para {sensor_code}: {e}")


def receive_data(client_socket, client_address, database_path, sensor_codes_map):
    conn = create_connection(database_path)
    if not conn:
        client_socket.close()
        return

    print(f"[+] Cliente conectado: {client_address[0]}:{client_address[1]}")

    try:
        while True:
            request = client_socket.recv(4096)
            if not request:
                print(f"[-] Cliente desconectado: {client_address[0]}:{client_address[1]}")
                break

            try:
                lote = json.loads(request.decode("utf-8"))
                timestamp = lote.get("timestamp", time.strftime("%Y-%m-%d %H:%M:%S"))
                datos = lote.get("datos", {})

                for short_code, valor in datos.items():
                    if short_code not in sensor_codes_map.values():
                        print(f"⚠ Sensor no registrado: {short_code}")
                        continue

                    try:
                        valor = round(float(valor),2)
                        insertar_datos(conn, short_code, valor, timestamp)
                        check_for_alerts(short_code, valor)
                    except ValueError:
                        print(f"⚠ Error: Valor no numérico '{valor}' para {short_code}")

                client_socket.send(b"accepted")

            except json.JSONDecodeError as e:
                print(f"⚠ Error al decodificar JSON: {e}")
                client_socket.send(b"error")

    except ConnectionResetError:
        print(f"[-] Cliente se desconectó abruptamente: {client_address[0]}:{client_address[1]}")
    finally:
        client_socket.close()
        conn.close()


def run_server():
    try:
        if not os.path.exists(CONFIG_FILE_PATH):
            raise FileNotFoundError(f"El archivo '{CONFIG_FILE_PATH}' no se encontró.")

        with open(CONFIG_FILE_PATH, 'r') as f:
            sensores_config = json.load(f)

        SENSOR_CODES_MAP = {
            str(i): sensor_data['short_code']
            for i, (key, sensor_data) in enumerate(sensores_config.items())
        }
        print(f"Diccionario de sensores cargado: {SENSOR_CODES_MAP}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    except json.JSONDecodeError:
        print("Error: El archivo config.json no es un JSON válido.")
        return

    database = "db.sqlite3"
    server_ip = "127.0.0.1"
    port = 8002   # ⚠ usar distinto al gateway (ej: 8003)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, port))
    server.listen(5)
    print(f"[+] Servidor escuchando en {server_ip}:{port}")

    try:
        while True:
            client_socket, client_address = server.accept()
            hilo = threading.Thread(target=receive_data,
                                    args=(client_socket, client_address, database, SENSOR_CODES_MAP))
            hilo.daemon = True
            hilo.start()
    except KeyboardInterrupt:
        print("\n[!] Servidor detenido por el usuario")
    finally:
        server.close()


if __name__ == '__main__':
    run_server()

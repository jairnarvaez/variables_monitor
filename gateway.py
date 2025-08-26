import socket
import threading
import time
import json

GATEWAY_IP = "127.0.0.1"
GATEWAY_PORT = 8001   
SERVER_IP = "127.0.0.1"
SERVER_PORT = 8002    

INTERVALO_LOTE = 2

lotes_buffer = {}
lock = threading.Lock()


def manejar_cliente(conn, addr):
    print(f"[+] Sensor conectado desde {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            mensaje = data.decode("utf-8").strip()

            partes = mensaje.split(",")
            if len(partes) == 3:
                key, valor, timestamp_csv = partes
                with lock:
                    if timestamp_csv not in lotes_buffer:
                        lotes_buffer[timestamp_csv] = {}
                    lotes_buffer[timestamp_csv][key] = valor
                print(f"[GATEWAY] Recibido: {key} = {valor} @ {timestamp_csv}")
            else:
                print(f"[GATEWAY] Formato inválido: {mensaje}")
            conn.send(b"OK")
    except Exception as e:
        print(f"[!] Error con sensor {addr}: {e}")
    finally:
        conn.close()
        print(f"[x] Sensor desconectado {addr}")


def enviar_al_servidor(lote):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            mensaje = json.dumps(lote)
            s.sendall(mensaje.encode("utf-8"))
            print(f"[GATEWAY -> SERVIDOR] Enviado: {mensaje}")
    except Exception as e:
        print(f"[!] No se pudo enviar el lote al servidor: {e}")


def procesar_lotes():
    while True:
        time.sleep(INTERVALO_LOTE)
        with lock:
            if lotes_buffer:
                with open("lotes.json", "a", encoding="utf-8") as f:
                    for ts, datos in lotes_buffer.items():
                        lote = {"timestamp": ts, "datos": datos}
                        json.dump(lote, f, ensure_ascii=False)
                        f.write("\n")
                        print(f"\n\t\t[LOTE] Guardado en JSON: {lote}")
                        enviar_al_servidor(lote)
                lotes_buffer.clear()
            else:
                print("[LOTE] No llegaron datos en este intervalo.")


def servidor_gateway():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((GATEWAY_IP, GATEWAY_PORT))
    server.listen(5)
    print(f"[GATEWAY] Escuchando sensores en {GATEWAY_IP}:{GATEWAY_PORT}")

    while True:
        conn, addr = server.accept()
        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
        hilo.daemon = True
        hilo.start()


if __name__ == "__main__":
    print("Iniciando Gateway (por lotes con timestamp del CSV)...")
    hilo_servidor = threading.Thread(target=servidor_gateway, daemon=True)
    hilo_servidor.start()

    procesar_lotes()

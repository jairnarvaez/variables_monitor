#!/bin/bash

# El script aún no está terminado :(

echo "[INIT] Ejecutando servidor.py..."
python3 servidor.py &
PID_SERVER=$!
sleep 2

echo "[INIT] Ejecutando gateway.py..."
python3 gateway.py &
PID_GATEWAY=$!
sleep 2

echo "[INIT] Ejecutando simulate_sensors.py con parámetros: $@"
python3 simulate_sensors.py "$@" &
PID_SENSORS=$!

cleanup() {
    echo -e "\n[STOP] Deteniendo todos los procesos..."
    kill $PID_SERVER $PID_GATEWAY $PID_SENSORS 2>/dev/null
    wait $PID_SERVER $PID_GATEWAY $PID_SENSORS 2>/dev/null
    echo "[STOP] Todo detenido correctamente."
    exit 0
}

trap cleanup SIGINT

wait

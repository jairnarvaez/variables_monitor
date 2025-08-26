#!/bin/bash

# Script para iniciar el sistema IoT
# Uso: ./run.sh [parametros_simulacion]
# Ejemplo: ./run.sh sensores.csv 5

# Iniciar el servidor
echo "[INIT] Ejecutando servidor.py..."
python3 servidor.py &
PID_SERVER=$!
sleep 2

# Iniciar el gateway
echo "[INIT] Ejecutando gateway.py..."
python3 gateway.py &
PID_GATEWAY=$!
sleep 2

# Iniciar los sensores simulados con los parámetros recibidos
echo "[INIT] Ejecutando simulate_sensors.py con parámetros: $@"
python3 simulate_sensors.py "$@" &
PID_SENSORS=$!

# Función para terminar todo cuando el usuario presione CTRL+C
cleanup() {
    echo -e "\n[STOP] Deteniendo todos los procesos..."
    kill $PID_SERVER $PID_GATEWAY $PID_SENSORS 2>/dev/null
    wait $PID_SERVER $PID_GATEWAY $PID_SENSORS 2>/dev/null
    echo "[STOP] Todo detenido correctamente."
    exit 0
}

# Capturar CTRL+C
trap cleanup SIGINT

# Esperar a que los procesos terminen (se controla con CTRL+C)
wait

import json
import os
from main_menu.models import Alerta 

CONFIG_FILE_PATH = "main_menu/config/config.json"

try:
    with open(CONFIG_FILE_PATH, 'r') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error al cargar el archivo de configuración: {e}")
    config = {}

THRESHOLDS = {
    data['short_code']: data['threshold']
    for data in config.values()
    if 'threshold' in data
}

def check_for_alerts(sensor_code, value):

    if sensor_code in THRESHOLDS:
    
        min_val = THRESHOLDS[sensor_code]['min']
        max_val = THRESHOLDS[sensor_code]['max']

        if not (min_val <= value <= max_val):
            message = f"Valor fuera de rango: {value} para el sensor."
            
            Alerta.objects.create(
                sensor_type=sensor_code,
                message=message,
                value=value,
                is_resolved = 0 
            )
            print(f"ALERTA GENERADA: {message}")
            return True
    
    return False

from django.db import models
import json
import os
from django.conf import settings

CONFIG_PATH = 'main_menu/config/'
config_file_path = os.path.join(settings.BASE_DIR, CONFIG_PATH, 'config.json')

SENSOR_CHOICES = []
try:
    with open(config_file_path, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
        for sensor_key, sensor_config in config_data.items():
            short_code = sensor_config.get('short_code')
            if short_code:
                SENSOR_CHOICES.append((short_code, sensor_config['name']))

except FileNotFoundError:
    print(f"Warning: Configuration file not found at {config_file_path}. Sensor choices will be empty.")

class SensorData(models.Model):
    sensor_type = models.CharField(max_length=10, choices=SENSOR_CHOICES)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Dato de Sensor"
        verbose_name_plural = "Datos de Sensores"

    def __str__(self):
        return f"{self.get_sensor_type_display()} - {self.value} ({self.timestamp.strftime('%Y-%m-%d %H:%M:%S')})"

class Alerta(models.Model):
    sensor_type = models.CharField(max_length=10)
    message = models.TextField()
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Alerta de {self.sensor_type} - {self.timestamp}"

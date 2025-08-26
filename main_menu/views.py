from django.shortcuts import render
from django.http.response import JsonResponse
from django.utils import timezone
from random import randint
from django.conf import settings
import os
import json
from .models import SensorData,  Alerta
from django.db.models import Avg, Min, Max
from django.core import serializers

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

CONFIG_PATH = 'main_menu/config/'
    
BASE_CHART_LINE_CONFIG = {
    'tooltip': {
        'trigger': 'axis'
    },
    'legend': {
        'top': 'bottom',
        'left': 0
    },
    'toolbox': {
        'top': 'bottom',
        'show': 'true',
        'feature': {
            'dataZoom': {
                'yAxisIndex': 'none'
            },
            'dataView': {'readOnly': 'false'},
            'magicType': {'type': ['line', 'bar']},
            'restore': {},
            'saveAsImage': {}
        }
    },
    'xAxis': {
        'type': 'category',
        'boundaryGap': 'false',
    },
    'yAxis': {
        'type': 'value',
    },
    'series': [
        {
            'type': 'line',
            'smooth': 'true',
            'markLine': {
                'data': [
                    {'type': 'average', 'name': 'Avg'},
                    [
                        {
                            'symbol': 'none',
                            'x': '90%',
                            'yAxis': 'max'
                        },
                        {
                            'symbol': 'circle',
                            'label': {
                                'position': 'start',
                                'formatter': 'Max'
                            },
                            'type': 'max',
                            'name': '最高点'
                        }
                    ]
                ]
            }
        }
    ]
}

def main_menu(request):
    titulo = "AgriTech"
    alertas = Alerta.objects.all().order_by('-timestamp') 

    print("Abriendo: ",  os.path.join(settings.BASE_DIR, CONFIG_PATH, 'config.json'))
    config_file_path = os.path.join(settings.BASE_DIR, CONFIG_PATH, 'config.json')
    
    with open(config_file_path, 'r') as f:
        config_sensores = json.load(f)

    umbrales = {
        data['short_code']: {
            'min': data['threshold']['min'],
            'max': data['threshold']['max'],
            'unit': data['unit']
        }
        for data in config_sensores.values()
    }
    
    context = {
        'titulo' : titulo,
        'width': 'w-20',
        'alertas': alertas,
        'umbrales': umbrales,
        'breadcrumb_titulo': 'Alertas'
    }

    return render(request, 'index.html', context)


@csrf_exempt  # Temporalmente para pruebas
@require_POST
def resolve_alert(request):
    try:
        data = json.loads(request.body)
        alert_id = data.get('alert_id')
        comment = data.get('comment', '') # Obtiene el comentario, o un string vacío si no se encuentra
        
        alert = Alerta.objects.get(pk=alert_id)
        alert.is_resolved = True
        alert.message = comment # ¡Guarda el comentario en el campo 'message'!
        alert.save()

        return JsonResponse({'success': True, 'message': 'Alerta resuelta correctamente.'})
    except Alerta.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Alerta no encontrada.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

try:
    print("Abriendo: ",  os.path.join(settings.BASE_DIR, CONFIG_PATH, 'config.json'))
    config_file_path = os.path.join(settings.BASE_DIR, CONFIG_PATH, 'config.json')
    with open(config_file_path, 'r', encoding='utf-8') as f:
        GRAPH_CONFIG = json.load(f)
except FileNotFoundError:
    GRAPH_CONFIG = {}  
    print("Warning: config.json file not found. Graph configuration will be empty.")

try:
    config_file_path = os.path.join(settings.BASE_DIR, CONFIG_PATH, 'config.json')
    with open(config_file_path, 'r', encoding='utf-8') as f:
        GRAPH_CONFIG = json.load(f)
except FileNotFoundError:
    GRAPH_CONFIG = {}
    print("Warning: config.json file not found. Graph configuration will be empty.")





SENSOR_CODE_MAP = {
    key: value['short_code'] for key, value in GRAPH_CONFIG.items()
}

def get_alerts_json(request):
    alerts = Alerta.objects.all().order_by('-timestamp')[:50]
    alerts_json_string = serializers.serialize('json', alerts, fields=('sensor_type', 'value', 'message', 'timestamp', 'is_resolved', 'id'))
    alerts_data = json.loads(alerts_json_string)
    return JsonResponse(alerts_data, safe=False)

def get_sensors_config(request):
    config_file_path = os.path.join(settings.BASE_DIR, CONFIG_PATH, 'config.json')
    try:
        with open(config_file_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
            return JsonResponse(config_data)
    except FileNotFoundError:
        return JsonResponse({'error': 'Configuración de sensores no encontrada.'}, status=404)



def get_sensor_configs():
    config_file_path = os.path.join(settings.BASE_DIR, CONFIG_PATH, 'config.json')
    try:
        with open(config_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Warning: config.json file not found. Graph configuration will be empty.")
        return {}

def get_sensor_code_map():
    configs = get_sensor_configs()
    return {
        key: value['short_code'] for key, value in configs.items()
    }



def get_data_and_stats2(sensor_name):
    # Call the function to get the latest sensor map
    sensor_code_map = get_sensor_code_map() 
    
    sensor_code = sensor_code_map.get(sensor_name)
    if not sensor_code:
        return None  

    queryset = SensorData.objects.filter(sensor_type=sensor_code).order_by('timestamp')
    data_values = list(queryset.values_list('value', flat=True))
    data_dates = [d.strftime('%Y-%m-%d %H:%M:%S') for d in queryset.values_list('timestamp', flat=True)]
    stats = queryset.aggregate(avg_value=Avg('value'), min_value=Min('value'), max_value=Max('value'))

    return {
        'data_dates': data_dates, 
        'data_values': data_values, 
        'stats': stats
    }


def get_dynamic_graph(request, sensor_name):
    # Call the function to get the latest sensor configs
    graph_config = get_sensor_configs()
    
    if sensor_name not in graph_config:
        return JsonResponse({'error': f'Sensor {sensor_name} not found.'}, status=404)

    config = graph_config[sensor_name]
    
    data = get_data_and_stats2(sensor_name)
    if not data:
        return JsonResponse({'error': f'Data for sensor "{sensor_name}" not found.'}, status=404)

    chart = BASE_CHART_LINE_CONFIG.copy()
    chart['xAxis']['data'] = data['data_dates']
    chart['yAxis']['axisLabel'] = {'formatter': f'{{value}} {config["unit"]}'}
    chart['series'][0]['name'] = config['name']
    chart['series'][0]['color'] = config['color']
    chart['series'][0]['data'] = data['data_values']
    
    return JsonResponse(chart)


def get_data_and_stats(sensor_name):
    
    sensor_code = SENSOR_CODE_MAP.get(sensor_name)
    if not sensor_code:
        return None 

    queryset = SensorData.objects.filter(sensor_type=sensor_code).order_by('timestamp')
    data_values = list(queryset.values_list('value', flat=True))
    data_dates = [d.strftime('%Y-%m-%d %H:%M:%S') for d in queryset.values_list('timestamp', flat=True)]
    stats = queryset.aggregate(avg_value=Avg('value'), min_value=Min('value'), max_value=Max('value'))

    return {
        'data_dates': data_dates, 
        'data_values': data_values, 
        'stats': stats
    }


def get_stats_json(request, model_name):
    stats_data = get_data_and_stats(model_name)
    if not stats_data:
        return JsonResponse({'error': f'Modelo "{model_name}" no encontrado.'}, status=404)

    return JsonResponse(stats_data['stats'])

#def get_dynamic_graph(request, sensor_name):
#    if sensor_name not in GRAPH_CONFIG:
 #       return JsonResponse({'error': f'Sensor {sensor_name} no encontrado.'}, status=404)
#
 #   config = GRAPH_CONFIG[sensor_name]
  #  
   # data = get_data_and_stats(sensor_name)
    #if not data:
     #   return JsonResponse({'error': f'Datos para el sensor "{sensor_name}" no encontrados.'}, status=404)

   # chart = BASE_CHART_LINE_CONFIG.copy()
   # chart['xAxis']['data'] = data['data_dates']
   # chart['yAxis']['axisLabel'] = {'formatter': f'{{value}} {config["unit"]}'}
   # chart['series'][0]['name'] = config['name']
   # chart['series'][0]['color'] = config['color']
   # chart['series'][0]['data'] = data['data_values']
    
   # return JsonResponse(chart)


def read_data_base(model):
    data_date = list(model.objects.values_list('data_date', flat=True))
    data_value = list(model.objects.values_list('data_value', flat=True))
    return data_date, data_value


@csrf_exempt
def add_sensor(request):

    print("Abriendo: ",  os.path.join(settings.BASE_DIR, CONFIG_PATH, 'config.json'))
    config_file_path = os.path.join(settings.BASE_DIR, CONFIG_PATH, 'config.json')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sensor_name_key = data['name'].lower().replace(" ", "_") # Ejemplo: 'Temperatura' -> 'temperatura'
            
            # Carga el archivo JSON actual
            with open(config_file_path, 'r+') as file:
                config_data = json.load(file)
            
            # Agrega el nuevo sensor
            config_data[sensor_name_key] = {
                "short_code": data['short_code'],
                "name": data['name'],
                "color": data['color'],
                "unit": data['unit'],
                "icon": data['icon'],
                "gradient": data['gradient'],
                "threshold": {
                    "min": data['threshold']['min'],
                    "max": data['threshold']['max']
                }
            }

            # Guarda el archivo JSON actualizado
            with open(config_file_path, 'w') as file:
                json.dump(config_data, file, indent=4)
            
            return JsonResponse({'success': True})
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})




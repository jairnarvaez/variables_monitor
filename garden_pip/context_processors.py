
import datetime
from django.db.models import Max
from main_menu.models import SensorData  

def navigation_info(request):
    """
    Procesador de contexto para agregar información de navegación global.
    """
    return {
        'app_1': 'Dashboard',
        'app_2': 'Noticias',
        'app_3': 'Gestor de Tareas',
        'app_4': 'Notificaciones',
        'app_5': 'Iniciar Sesión',
        'titulo': 'Agronomo'
    }

def global_status(request):
    try:
        latest_data = SensorData.objects.latest('timestamp')
        last_update = latest_data.timestamp
    except SensorData.DoesNotExist:
        last_update = datetime.datetime.now() 

    active_alerts = 0 
    
    return {
        'last_update_time': last_update,
        'active_alerts_count': active_alerts,
    }

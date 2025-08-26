# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_menu, name='main_menu'),
    
    path('get_graph/<str:sensor_name>/', views.get_dynamic_graph, name='get_dynamic_graph'),
    
    path('get_stats/<str:model_name>/', views.get_stats_json, name='get_stats_json'),

    path('get_sensors_config/', views.get_sensors_config, name='get_sensors_config'),
    path('get_alerts_json/', views.get_alerts_json, name='get_alerts_json'),

    path("resolve_alert/<int:alert_id>/", views.resolve_alert, name="resolve_alert"),

    path('resolve_alert/', views.resolve_alert, name='resolve_alert'),  

    path('add_sensor/', views.add_sensor, name='add_sensor'),
]

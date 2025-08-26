# 🌱 AgriTech – Plataforma de Monitoreo Ambiental

AgriTech es una plataforma desarrollada en el marco de un proyecto de integración profesional.  
Su objetivo es **monitorear variables ambientales de una huerta comunitaria** mediante una estación meteorológica.  

El sistema está estructurado en tres componentes principales:  
1. **Servidor** – Desarrollado en Django, gestiona la interfaz web y la base de datos.  
2. **Gateway** – Recibe los datos de los sensores y los transmite al servidor.  
3. **Red de Sensores** – Captura datos ambientales (en este repositorio se simula mediante archivos CSV).  

Este repositorio contiene el **código fuente del servidor** y scripts de simulación para el gateway y los sensores.  


## 🚀 Guía de Configuración y Ejecución

Proyecto en **Django** para monitorear variables de sensores.  
Este repositorio contiene el código fuente y los recursos necesarios para ejecutar la aplicación localmente.


### **1. Requisitos del Sistema**

Asegúrate de tener instalados los siguientes programas en tu sistema:

* **Python 3.x**
* **pip** (el gestor de paquetes de Python)
* **Git**

### **2. Clonar el Repositorio**

Usa `git` para obtener el código fuente del proyecto en tu máquina.

```bash
git clone https://github.com/jairnarvaez/variables_monitor.git
cd variables_monitor
```

### **3. Configuración del Entorno Virtual**

```python
python -m venv venv
source venv/bin/activate
```

### **4. Instalación dependencias**

```python
pip install -r requirements.txt
```

### **4. Migraciones a la base de datos**
```python
python manage.py makemigrations
python manage.py migrate
```

### **5. Ejecutar el servidor**
```python
python manage.py runserver
```
### **6. Simulacion de sensores**
El algoritmo que se encarga de recibir los datos de los sensores es servidor.py asi que para ponerlo a la escucha de las peticiones ejecuta:
```python
python servidor.py
```
Ahora bien, a fin de poder probar la interfaz  se diseño un algoritmo que permite simular el comportamiento del gateway que fue usado en el proyecto para usarlo ejecuta:
```python
python servidor.py
```
Finalmente, para que puedas probar el proyecto tambien se diseño unarchivo que simula los sensores, los datos son los archivos obtenidos en el archi clima.csv debes ejectuar:
Ahora bien, a fin de poder probar la interfaz  se diseño un algoritmo que permite simular el comportamiento del gateway que fue usado en el proyecto para usarlo ejecuta:
```python
python simulate_sensors.py
```

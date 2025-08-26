# 🌱 AgriTech – Plataforma de Monitoreo Ambiental

AgriTech es una plataforma desarrollada en el marco de un proyecto de integración profesional.  
Su objetivo es **monitorear variables ambientales de una huerta comunitaria** mediante una estación meteorológica.  

El sistema se estructuró en tres componentes principales:  
1. **Servidor** – Desarrollado en Django, gestiona la interfaz web y la base de datos.  
2. **Gateway** – Recibe los datos de los sensores y los transmite al servidor, implementado en una Raspberry PI 4  
3. **Red de Sensores** – Captura datos ambientales  usando como plataforma Arduino  (en este repositorio se simula mediante archivos CSV). 

Aunque este repositorio solamente contiene el **código fuente del servidor**, se incluyen algunos scripts que permiten la simulación para el gateway y los sensores.  

## 🚀 Guía de Configuración y Ejecución
 
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

```bash
python -m venv venv
source venv/bin/activate
```

### **4. Instalación dependencias**

```bash
pip install -r requirements.txt
```

### **4. Migraciones a la base de datos**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **5. Ejecutar el servidor**
```bash
python manage.py runserver
```
### **6. Simulacion de sensores**
El proyecto incluye scripts que permiten **probar el sistema sin necesidad de hardware real**.  
La comunicación entre los componentes se realiza en tres pasos:
1. **Iniciar el servidor TCP**  
   Este módulo recibe los datos provenientes del gateway.  
```bash
python servidor.py
```
2. **Ejecutar la simulación del Gateway**
El gateway actúa como intermediario entre los sensores y el servidor.
```bash
python gateway.py
```
3. **Ejecutar la simulación de Sensores**
Este script toma los datos desde el archivo clima.csv y los envía al gateway, emulando el funcionamiento de los sensores físicos.
```bash
python simulate_sensors.py
```

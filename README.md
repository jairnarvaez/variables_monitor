# Nombre de tu Proyecto

Una descripción breve y concisa de lo que hace tu proyecto. ¿Cuál es su propósito? ¿Qué problema resuelve?

---

## 🚀 Guía de Configuración y Ejecución

Esta guía te ayudará a poner en marcha este proyecto de manera local.

### **1. Requisitos del Sistema**

Asegúrate de tener instalados los siguientes programas en tu sistema:

* **Python 3.x**
* **pip** (el gestor de paquetes de Python)
* **Git**

### **2. Clonar el Repositorio**

Usa `git` para obtener el código fuente del proyecto en tu máquina.

```bash
git clone <url_del_repositorio>
cd <nombre_del_directorio_del_proyecto>
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


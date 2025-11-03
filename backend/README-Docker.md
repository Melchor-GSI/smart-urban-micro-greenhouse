# IoT Backend - Despliegue con Docker

Este proyecto Flask ha sido configurado para ejecutarse con Docker.

## 🐳 Opciones de Despliegue

### Opción 1: Docker Compose (Recomendado)

```bash
# Construir y ejecutar el contenedor
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Parar los servicios
docker-compose down
```

### Opción 2: Docker directamente

```bash
# Construir la imagen
docker build -t iot-backend .

# Ejecutar el contenedor
docker run -p 5001:5001 --name iot-backend-container iot-backend

# Ejecutar en segundo plano
docker run -d -p 5001:5001 --name iot-backend-container iot-backend

# Ver logs
docker logs -f iot-backend-container

# Parar el contenedor
docker stop iot-backend-container

# Eliminar el contenedor
docker rm iot-backend-container
```

## 🔧 Configuración

### Variables de Entorno

Puedes personalizar la configuración usando variables de entorno:

```bash
# En docker-compose.yml
environment:
  - FLASK_ENV=production
  - FLASK_APP=app.py
  - SECRET_KEY=tu-clave-secreta-aqui
```

### Persistencia de Datos

Si necesitas persistir datos, descomenta las líneas de volúmenes en `docker-compose.yml`:

```yaml
volumes:
  - ./data:/app/data
```

## 🏥 Health Check

El contenedor incluye un health check que verifica cada 30 segundos que la aplicación esté funcionando correctamente.

## 📝 Logs

Para ver los logs de la aplicación:

```bash
# Con docker-compose
docker-compose logs -f backend

# Con docker directamente
docker logs -f iot-backend-container
```

## 🚀 Producción

En producción, la aplicación usa Gunicorn como servidor WSGI para mejor rendimiento:

- 4 workers
- 2 threads por worker
- Timeout de 120 segundos
- Keep-alive de 2 segundos
- Máximo 1000 requests por worker

## 🔒 Seguridad

- La aplicación se ejecuta con un usuario no-root
- Se minimizan las dependencias del sistema
- Health checks incluidos

## 📋 Requisitos

- Docker
- Docker Compose (para la opción recomendada)

## 🌐 Acceso

Una vez ejecutado, la aplicación estará disponible en:
- http://localhost:5001

## 🛠️ Desarrollo

Para desarrollo local sin Docker, puedes seguir usando:

```bash
pip install -r requirements.txt
python app.py
```
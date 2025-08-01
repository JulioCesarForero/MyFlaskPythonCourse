# Comandos útiles para desarrollo con Docker

## Configuración inicial

1. **Copia el archivo de configuración:**
   ```powershell
   copy .env.example .env
   ```

2. **Genera una clave JWT segura:**
   ```powershell
   python generate_jwt_key.py
   ```
   Copia el resultado en tu archivo `.env`

3. **Edita el archivo `.env`** con tus configuraciones específicas

## Desarrollo rápido (recomendado)
```powershell
# Iniciar en modo desarrollo (hot reload activado)
docker-compose up --build

# Ejecutar en background
docker-compose up -d --build

# Ver logs en tiempo real
docker-compose logs -f web

# Parar los servicios
docker-compose down

# Reiniciar solo el servicio web
docker-compose restart web
```

## Comandos para optimizar desarrollo

```powershell
# Construcción más rápida (sin caché si hay problemas)
docker-compose build --no-cache web

# Eliminar contenedores e imágenes huérfanas
docker-compose down --rmi local --volumes --remove-orphans

# Limpiar todo el sistema Docker (usar con cuidado)
docker system prune -a -f
```

## Flujo de desarrollo optimizado

1. **Primera vez o cambios en requirements.txt:**
   ```powershell
   docker-compose up --build
   ```

2. **Desarrollo diario (sin cambios en dependencias):**
   ```powershell
   docker-compose up
   ```

3. **Cambios solo en código Python:**
   - No necesitas reconstruir, Flask detectará los cambios automáticamente

4. **Ver la aplicación:**
   - http://localhost:5005
   - Swagger UI: http://localhost:5005/swagger-ui

## Variables de entorno

El proyecto usa un archivo `.env` para la configuración. Variables importantes:

- `JWT_SECRET_KEY`: Clave secreta para JWT (generar con `python generate_jwt_key.py`)
- `DATABASE_URL`: URL de la base de datos
- `FLASK_ENV`: Entorno de Flask (development/production)
- `FLASK_DEBUG`: Activar modo debug

## Optimizaciones implementadas

✅ **Cache de Docker optimizado** - Las dependencias se instalan antes que el código
✅ **Hot reload activado** - Los cambios en código se reflejan inmediatamente  
✅ **Variables de entorno con .env** - Configuración segura y flexible
✅ **Volúmenes optimizados** - Excluye archivos innecesarios como __pycache__
✅ **Health check** - Verifica que la aplicación esté funcionando
✅ **Restart policy** - El contenedor se reinicia automáticamente si falla
✅ **.dockerignore optimizado** - Excluye archivos innecesarios del contexto de build
✅ **Generador de claves JWT** - Script para generar claves seguras

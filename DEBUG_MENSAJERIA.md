# Guía de Depuración - Sistema de Mensajería

## Cambios Realizados

### 1. Frontend (Flutter) - Logs de Depuración
- **Archivo**: `lib/features/mensajeria/services/mensajeria_service.dart`
- **Cambios**: Agregados logs detallados para rastrear:
  - URL completa de la petición
  - Headers enviados
  - Status code de respuesta
  - Tipo de datos recibidos
  - Errores específicos con detalles

### 2. Backend (FastAPI) - Logs de Depuración
- **Archivo**: `api/v1/routes_mensajeria.py`
- **Cambios**: Agregado manejo de errores con logs detallados en el endpoint `/conversaciones`

- **Archivo**: `services/mensajeria/conversacion_service.py`
- **Cambios**: 
  - Agregados logs en `obtener_conversaciones_usuario()`
  - Mejorado manejo de URLs de fotos de perfil usando SupabaseSettings
  - Agregado manejo de errores con traceback completo

## Cómo Verificar el Flujo

### Paso 1: Verificar que el API esté corriendo
```bash
# En la terminal del API
cd C:\GerzApps\IDGS1004\app-interface-InnPulse360
python main.py
```

Deberías ver algo como:
```
INFO:     Started server process
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Paso 2: Verificar que el endpoint esté registrado
Abre tu navegador y ve a:
```
http://127.0.0.1:8000/docs
```

Busca el endpoint `GET /api/v1/mensajeria/conversaciones` en la documentación de Swagger.

### Paso 3: Probar el endpoint directamente
Puedes probar el endpoint con curl o Postman:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/mensajeria/conversaciones?skip=0&limit=100" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

### Paso 4: Verificar logs en la app móvil
Cuando ejecutes la app móvil y navegues a la pantalla de mensajería, deberías ver en la consola de Flutter:

```
🔵 MensajeriaService: Obteniendo conversaciones desde: http://127.0.0.1:8000/api/v1/mensajeria/conversaciones
🔵 MensajeriaService: Headers: [Authorization, Content-Type]
🔵 MensajeriaService: Respuesta recibida - Status: 200
🔵 MensajeriaService: Tipo de datos: List<dynamic>
🔵 MensajeriaService: Conversaciones parseadas: X
```

### Paso 5: Verificar logs en el backend
En la terminal donde corre el API, deberías ver:

```
🔵 API: Obteniendo conversaciones para usuario_id=X, skip=0, limit=100
🔵 ConversacionService: Obteniendo conversaciones para usuario_id=X
🔵 ConversacionService: Encontradas X conversaciones en BD
🔵 ConversacionService: Retornando X conversaciones procesadas
🔵 API: Retornando X conversaciones
```

## Problemas Comunes y Soluciones

### Problema 1: Error de conexión
**Síntoma**: `Error de conexión. Verifica tu conexión a internet...`

**Causas posibles**:
1. El API no está corriendo
2. La URL base está incorrecta (`127.0.0.1` no funciona en dispositivos físicos)
3. Firewall bloqueando la conexión

**Solución**:
- Si estás usando un emulador Android, cambia `127.0.0.1` por `10.0.2.2` en `api_config.dart`
- Si estás usando un dispositivo físico, usa la IP local de tu máquina (ej: `192.168.1.100:8000`)
- Verifica que el API esté corriendo y accesible

### Problema 2: Error 401 (No autorizado)
**Síntoma**: `Error del servidor (401): Unauthorized`

**Causa**: Token de autenticación inválido o expirado

**Solución**:
- Verifica que el usuario esté autenticado correctamente
- Verifica que el token se esté enviando en los headers
- Re-autentica al usuario

### Problema 3: Error 500 (Error del servidor)
**Síntoma**: `Error del servidor (500): Error al obtener conversaciones...`

**Causa**: Error en el backend (base de datos, lógica, etc.)

**Solución**:
- Revisa los logs del backend para ver el error específico
- Verifica que las tablas de mensajería existan en la base de datos
- Verifica que el usuario tenga permisos para acceder a las conversaciones

### Problema 4: Error de parseo JSON
**Síntoma**: `Error parseando conversación: ...`

**Causa**: El formato de datos del backend no coincide con el modelo de Flutter

**Solución**:
- Compara el JSON recibido con el modelo `ConversacionModel`
- Verifica que todos los campos requeridos estén presentes
- Revisa los logs para ver el JSON exacto que está causando el error

## Verificación de la Base de Datos

### Verificar que las tablas existan
Ejecuta en SQL Server:
```sql
SELECT * FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = 'MENSAJERIA'
```

Deberías ver:
- `Tb_Conversacion`
- `Tb_Mensaje`
- `Tb_MensajeAdjunto`

### Verificar que haya datos
```sql
SELECT COUNT(*) FROM MENSAJERIA.Tb_Conversacion;
SELECT COUNT(*) FROM MENSAJERIA.Tb_Mensaje;
```

## Próximos Pasos

1. Ejecuta la app móvil y navega a la pantalla de mensajería
2. Revisa los logs tanto en Flutter como en el backend
3. Comparte los logs si encuentras algún error para poder diagnosticarlo mejor



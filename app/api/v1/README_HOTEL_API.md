# API de Hotel - Documentación

## Descripción General

Esta API proporciona operaciones CRUD (Create, Read, Update, Delete) completas para la gestión de hoteles, utilizando FastAPI y SQLAlchemy con una arquitectura en capas.

## Arquitectura

```
┌─────────────┐
│   Routes    │  ← Endpoints de la API (FastAPI)
└──────┬──────┘
       │
┌──────▼──────┐
│  Services   │  ← Lógica de negocio
└──────┬──────┘
       │
┌──────▼──────┐
│     DAO     │  ← Acceso a datos (SQLAlchemy)
└──────┬──────┘
       │
┌──────▼──────┐
│  Database   │  ← SQL Server
└─────────────┘
```

## Endpoints Disponibles

### 1. Obtener Todos los Hoteles
**GET** `/api/v1/hotel/`

**Parámetros de consulta:**
- `skip` (int, opcional): Número de registros a saltar (default: 0)
- `limit` (int, opcional): Número máximo de registros (default: 100, max: 1000)

**Respuesta exitosa (200):**
```json
[
  {
    "id_hotel": 1,
    "nombre": "Hotel Plaza Madrid",
    "direccion": "Calle Gran Vía, 123",
    "id_pais": 1,
    "id_estado": 15,
    "codigo_postal": "28013",
    "telefono": "+34 91 123 45 67",
    "email_contacto": "reservas@hotelplaza.com",
    "numero_estrellas": 4
  }
]
```

### 2. Obtener Hotel por ID
**GET** `/api/v1/hotel/{hotel_id}`

**Parámetros de ruta:**
- `hotel_id` (int): ID del hotel

**Respuestas:**
- 200: Hotel encontrado
- 404: Hotel no encontrado
- 500: Error del servidor

**Ejemplo de respuesta exitosa (200):**
```json
{
  "id_hotel": 1,
  "nombre": "Hotel Plaza Madrid",
  "direccion": "Calle Gran Vía, 123",
  "id_pais": 1,
  "id_estado": 15,
  "codigo_postal": "28013",
  "telefono": "+34 91 123 45 67",
  "email_contacto": "reservas@hotelplaza.com",
  "numero_estrellas": 4
}
```

### 3. Crear Nuevo Hotel
**POST** `/api/v1/hotel/`

**Cuerpo de la petición:**
```json
{
  "nombre": "Hotel Plaza Madrid",
  "direccion": "Calle Gran Vía, 123",
  "id_pais": 1,
  "id_estado": 15,
  "codigo_postal": "28013",
  "telefono": "+34 91 123 45 67",
  "email_contacto": "reservas@hotelplaza.com",
  "numero_estrellas": 4
}
```

**Campos requeridos:**
- `nombre` (string, 1-150 caracteres)
- `direccion` (string, 1-200 caracteres)
- `id_pais` (int, > 0)

**Campos opcionales:**
- `id_estado` (int, > 0)
- `codigo_postal` (string, max 20 caracteres)
- `telefono` (string, max 30 caracteres)
- `email_contacto` (string, max 150 caracteres, debe contener @)
- `numero_estrellas` (int, 1-5)

**Respuestas:**
- 201: Hotel creado exitosamente
- 400: Datos inválidos
- 500: Error del servidor

### 4. Actualizar Hotel
**PUT** `/api/v1/hotel/{hotel_id}`

**Parámetros de ruta:**
- `hotel_id` (int): ID del hotel a actualizar

**Cuerpo de la petición (todos los campos son opcionales):**
```json
{
  "nombre": "Hotel Plaza Madrid Centro",
  "telefono": "+34 91 987 65 43",
  "numero_estrellas": 5
}
```

**Respuestas:**
- 200: Hotel actualizado exitosamente
- 400: Datos inválidos
- 404: Hotel no encontrado
- 500: Error del servidor

### 5. Eliminar Hotel
**DELETE** `/api/v1/hotel/{hotel_id}`

**Parámetros de ruta:**
- `hotel_id` (int): ID del hotel a eliminar

**Respuestas:**
- 204: Hotel eliminado exitosamente (sin contenido)
- 404: Hotel no encontrado
- 500: Error del servidor

---

## Endpoints de Búsqueda Adicionales

### 6. Buscar por Nombre
**GET** `/api/v1/hotel/buscar/nombre/{nombre}`

Busca hoteles que contengan el texto especificado en su nombre.

**Ejemplo:**
```
GET /api/v1/hotel/buscar/nombre/Plaza
```

### 7. Obtener Hoteles por País
**GET** `/api/v1/hotel/pais/{id_pais}`

Obtiene todos los hoteles de un país específico.

**Ejemplo:**
```
GET /api/v1/hotel/pais/1
```

### 8. Obtener Hoteles por Estrellas
**GET** `/api/v1/hotel/estrellas/{numero_estrellas}`

Obtiene todos los hoteles con un número específico de estrellas (1-5).

**Ejemplo:**
```
GET /api/v1/hotel/estrellas/4
```

---

## Ejemplos de Uso con cURL

### Crear un hotel:
```bash
curl -X POST "http://localhost:8000/api/v1/hotel/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Hotel Plaza Madrid",
    "direccion": "Calle Gran Vía, 123",
    "id_pais": 1,
    "id_estado": 15,
    "codigo_postal": "28013",
    "telefono": "+34 91 123 45 67",
    "email_contacto": "reservas@hotelplaza.com",
    "numero_estrellas": 4
  }'
```

### Obtener todos los hoteles:
```bash
curl -X GET "http://localhost:8000/api/v1/hotel/?skip=0&limit=10"
```

### Obtener un hotel específico:
```bash
curl -X GET "http://localhost:8000/api/v1/hotel/1"
```

### Actualizar un hotel:
```bash
curl -X PUT "http://localhost:8000/api/v1/hotel/1" \
  -H "Content-Type: application/json" \
  -d '{
    "numero_estrellas": 5,
    "telefono": "+34 91 999 88 77"
  }'
```

### Eliminar un hotel:
```bash
curl -X DELETE "http://localhost:8000/api/v1/hotel/1"
```

---

## Estructura de Código

### DAO (Data Access Object) - `dao_hotel.py`
- Maneja todas las operaciones de base de datos
- Métodos principales:
  - `create()`: Crear nuevo hotel
  - `get_by_id()`: Obtener por ID
  - `get_all()`: Obtener todos con paginación
  - `update()`: Actualizar hotel
  - `delete()`: Eliminar hotel
  - Métodos de búsqueda adicionales

### Servicio - `hotel_service.py`
- Contiene la lógica de negocio
- Valida datos antes de enviar al DAO
- Maneja errores y excepciones
- Convierte modelos de base de datos a schemas de respuesta

### Rutas - `routes_hotel.py`
- Define los endpoints de la API
- Maneja peticiones HTTP
- Inyecta dependencias (servicio y sesión de BD)
- Retorna respuestas HTTP apropiadas

---

## Validaciones Implementadas

### Validaciones de Schema (Pydantic)
- **Nombre**: 1-150 caracteres, requerido
- **Dirección**: 1-200 caracteres, requerido
- **ID País**: Entero positivo, requerido
- **ID Estado**: Entero positivo, opcional
- **Código Postal**: Máximo 20 caracteres, opcional
- **Teléfono**: Máximo 30 caracteres, solo números y símbolos permitidos, opcional
- **Email**: Debe contener @, máximo 150 caracteres, opcional
- **Número de Estrellas**: Entre 1 y 5, opcional

### Validaciones de Negocio
- No se puede actualizar un hotel sin proporcionar al menos un campo
- El número de estrellas debe estar entre 1 y 5 al buscar por estrellas

---

## Manejo de Errores

La API implementa manejo robusto de errores:

- **400 Bad Request**: Datos de entrada inválidos
- **404 Not Found**: Recurso no encontrado
- **500 Internal Server Error**: Error del servidor/base de datos

Todos los errores incluyen un mensaje descriptivo en el campo `detail`.

---

## Documentación Interactiva

Una vez que la aplicación esté corriendo, puedes acceder a:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

Estas interfaces permiten probar todos los endpoints de forma interactiva.

---

## Notas Técnicas

1. **Inyección de Dependencias**: FastAPI se encarga de inyectar automáticamente la sesión de base de datos
2. **Cierre de Sesiones**: Las sesiones se cierran automáticamente después de cada petición
3. **Transacciones**: Todos los cambios se hacen en transacciones que se revierten automáticamente en caso de error
4. **Paginación**: Implementada en el endpoint de listar todos los hoteles para optimizar rendimiento
5. **Thread-Safe**: La conexión a base de datos usa el patrón Singleton con thread-safety

---

## Próximos Pasos

Para usar esta API:

1. Asegúrate de tener configurado el archivo `.development.env` con las credenciales de base de datos
2. Ejecuta la aplicación: `uvicorn app.main:app --reload`
3. Accede a `http://localhost:8000/docs` para ver y probar los endpoints
4. Comienza a realizar peticiones CRUD a los hoteles


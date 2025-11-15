# Documentación de API - InnPulse360

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Autenticación](#autenticación)
3. [Base URL](#base-url)
4. [Códigos de Estado HTTP](#códigos-de-estado-http)
5. [Endpoints por Módulo](#endpoints-por-módulo)
   - [Autenticación y Usuarios](#1-autenticación-y-usuarios)
   - [Hoteles](#2-hoteles)
     - [Tipos de Habitación](#29-tipos-de-habitación)
     - [Características](#210-características)
     - [Tipo Habitación-Característica](#211-tipo-habitación-característica)
     - [Pisos](#212-pisos)
     - [Habitación Área](#213-habitación-área)
   - [Clientes](#3-clientes)
   - [Reservaciones](#4-reservaciones)
     - [Tipos de Cargo](#41-tipos-de-cargo)
     - [Cargos](#42-cargos)
     - [Servicios de Transporte](#43-servicios-de-transporte)
     - [Cargo-Servicio Transporte](#44-cargo-servicio-transporte)
   - [Empleados](#5-empleados)
   - [Limpieza (Camarista)](#6-limpieza-camarista)
     - [Tipos de Limpieza](#69-tipos-de-limpieza)
     - [Estatus de Limpieza](#610-estatus-de-limpieza)
   - [Mantenimiento](#7-mantenimiento)
     - [Incidencias](#79-incidencias)
   - [Catálogos](#8-catálogos)
     - [Periodicidades](#83-periodicidades)
   - [Email](#9-email)
   - [Almacenamiento de Imágenes](#10-almacenamiento-de-imágenes)
     - [Imágenes de Hoteles](#102-imágenes-de-hoteles)
     - [Imágenes de Habitaciones](#103-imágenes-de-habitaciones)
     - [Imágenes de Limpieza](#104-imágenes-de-limpieza)
     - [Imágenes de Mantenimiento](#105-imágenes-de-mantenimiento)
     - [Imágenes de Tipo de Habitación](#106-imágenes-de-tipo-de-habitación)
     - [Imágenes de Incidencias](#107-imágenes-de-incidencias)
   - [Seguridad y Roles](#11-seguridad-y-roles)
     - [Usuario-Rol](#112-usuario-rol)
     - [Módulos](#113-módulos)

---

## Introducción

Esta documentación describe todos los endpoints disponibles en la API de InnPulse360. La API está construida con FastAPI y utiliza autenticación basada en tokens JWT (JSON Web Tokens).

### Características Principales

- **RESTful API**: Todos los endpoints siguen los principios REST
- **Autenticación JWT**: La mayoría de endpoints requieren autenticación mediante Bearer Token
- **Validación Automática**: Validación de datos de entrada mediante Pydantic
- **Documentación Interactiva**: Disponible en `/docs` (Swagger) y `/redoc`
- **Versionado**: API versionada en `/api/v1`

---

## Autenticación

### Obtener Token de Acceso

La mayoría de los endpoints requieren autenticación mediante un token JWT. Para obtener el token, primero debes autenticarte:

**Endpoint**: `POST /api/v1/usuarios/login`

**Request Body**:
```json
{
  "login": "juan.perez",
  "password": "tu_contraseña"
}
```

**Response Exitosa (200 OK)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "usuario": {
    "id_usuario": 1,
    "login": "juan.perez",
    "correo_electronico": "juan.perez@email.com"
  },
  "modulos": [
    {
      "id_modulo": 1,
      "nombre": "Dashboard",
      "descripcion": "Panel principal",
      "icono": "fas fa-dashboard",
      "ruta": "/dashboard"
    }
  ],
  "password_temporal_info": null
}
```

### Usar el Token

Una vez obtenido el token, inclúyelo en el header `Authorization` de todas las peticiones:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Ejemplo con cURL**:
```bash
curl -X GET "http://localhost:8000/api/v1/hotel/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Ejemplo con JavaScript (fetch)**:
```javascript
fetch('http://localhost:8000/api/v1/hotel/', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
    'Content-Type': 'application/json'
  }
})
```

### Expiración del Token

- **Duración**: 30 minutos (1800 segundos)
- **Renovación**: Debes volver a autenticarte para obtener un nuevo token
- **Error 401**: Si el token ha expirado, recibirás un error 401 Unauthorized

---

## Base URL

**Desarrollo**: `http://localhost:8000`  
**Producción**: `https://api.innpulse360.com`

Todos los endpoints están bajo el prefijo: `/api/v1`

---

## Códigos de Estado HTTP

| Código | Significado | Descripción |
|--------|-------------|-------------|
| 200 | OK | Petición exitosa |
| 201 | Created | Recurso creado exitosamente |
| 204 | No Content | Operación exitosa sin contenido de respuesta |
| 400 | Bad Request | Datos inválidos en la petición |
| 401 | Unauthorized | Token inválido o ausente |
| 404 | Not Found | Recurso no encontrado |
| 500 | Internal Server Error | Error interno del servidor |

---

## Endpoints por Módulo

---

## 1. Autenticación y Usuarios

### 1.1. Iniciar Sesión

**Endpoint**: `POST /api/v1/usuarios/login`

**Objetivo**: Autenticar un usuario y obtener un token JWT de acceso.

**Autenticación**: No requerida

**Request Body**:
```json
{
  "login": "juan.perez",
  "password": "Password123"
}
```

**Parámetros**:
- `login` (string, requerido): Login del usuario (máximo 25 caracteres)
- `password` (string, requerido): Contraseña del usuario

**Response Exitosa (200 OK)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzA5ODc2MDAwfQ...",
  "token_type": "bearer",
  "expires_in": 1800,
  "usuario": {
    "id_usuario": 1,
    "login": "juan.perez",
    "correo_electronico": "juan.perez@email.com"
  },
  "modulos": [
    {
      "id_modulo": 1,
      "nombre": "Dashboard",
      "descripcion": "Panel principal del sistema",
      "icono": "fas fa-dashboard",
      "ruta": "/dashboard"
    }
  ],
  "password_temporal_info": null
}
```

**Errores Posibles**:
- `401 Unauthorized`: Credenciales inválidas
- `400 Bad Request`: Datos de entrada inválidos

**Ejemplo cURL**:
```bash
curl -X POST "http://localhost:8000/api/v1/usuarios/login" \
  -H "Content-Type: application/json" \
  -d '{
    "login": "juan.perez",
    "password": "Password123"
  }'
```

---

### 1.2. Crear Usuario

**Endpoint**: `POST /api/v1/usuarios/`

**Objetivo**: Crear un nuevo usuario en el sistema.

**Autenticación**: Requerida

**Request Body**:
```json
{
  "login": "nuevo.usuario",
  "correo_electronico": "nuevo@email.com",
  "password": "Password123",
  "estatus_id": 1
}
```

**Parámetros**:
- `login` (string, requerido): Login único del usuario (máximo 25 caracteres)
- `correo_electronico` (string, requerido): Email único del usuario (máximo 50 caracteres)
- `password` (string, requerido): Contraseña (mínimo 6 caracteres, se encripta automáticamente)
- `estatus_id` (integer, opcional): Estatus del usuario (1=Activo por defecto)

**Response Exitosa (201 Created)**:
```json
{
  "id_usuario": 5,
  "login": "nuevo.usuario",
  "correo_electronico": "nuevo@email.com",
  "estatus_id": 1
}
```

**Errores Posibles**:
- `400 Bad Request`: Login o email ya existe, o datos inválidos
- `401 Unauthorized`: Token inválido o ausente

**Ejemplo cURL**:
```bash
curl -X POST "http://localhost:8000/api/v1/usuarios/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "login": "nuevo.usuario",
    "correo_electronico": "nuevo@email.com",
    "password": "Password123",
    "estatus_id": 1
  }'
```

---

### 1.3. Listar Usuarios

**Endpoint**: `GET /api/v1/usuarios/`

**Objetivo**: Obtener lista de todos los usuarios con paginación.

**Autenticación**: Requerida

**Query Parameters**:
- `skip` (integer, opcional): Número de registros a saltar (default: 0)
- `limit` (integer, opcional): Número máximo de registros (default: 100, máximo: 1000)

**Response Exitosa (200 OK)**:
```json
[
  {
    "id_usuario": 1,
    "login": "juan.perez",
    "correo_electronico": "juan.perez@email.com",
    "estatus_id": 1
  },
  {
    "id_usuario": 2,
    "login": "maria.garcia",
    "correo_electronico": "maria@email.com",
    "estatus_id": 1
  }
]
```

**Ejemplo cURL**:
```bash
curl -X GET "http://localhost:8000/api/v1/usuarios/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 1.4. Obtener Usuario por ID

**Endpoint**: `GET /api/v1/usuarios/{id_usuario}`

**Objetivo**: Obtener información de un usuario específico.

**Autenticación**: Requerida

**Path Parameters**:
- `id_usuario` (integer, requerido): ID del usuario

**Response Exitosa (200 OK)**:
```json
{
  "id_usuario": 1,
  "login": "juan.perez",
  "correo_electronico": "juan.perez@email.com",
  "estatus_id": 1
}
```

**Errores Posibles**:
- `404 Not Found`: Usuario no encontrado

---

### 1.5. Actualizar Usuario

**Endpoint**: `PUT /api/v1/usuarios/{id_usuario}`

**Objetivo**: Actualizar información de un usuario existente (actualización parcial).

**Autenticación**: Requerida

**Path Parameters**:
- `id_usuario` (integer, requerido): ID del usuario a actualizar

**Request Body** (todos los campos son opcionales):
```json
{
  "login": "nuevo.login",
  "correo_electronico": "nuevo@email.com",
  "password": "NuevaPassword123",
  "estatus_id": 1
}
```

**Response Exitosa (200 OK)**:
```json
{
  "id_usuario": 1,
  "login": "nuevo.login",
  "correo_electronico": "nuevo@email.com",
  "estatus_id": 1
}
```

**Nota**: Si se proporciona una nueva contraseña, se encripta automáticamente.

---

### 1.6. Eliminar Usuario

**Endpoint**: `DELETE /api/v1/usuarios/{id_usuario}`

**Objetivo**: Eliminar un usuario (eliminación lógica - cambia estatus a inactivo).

**Autenticación**: Requerida

**Path Parameters**:
- `id_usuario` (integer, requerido): ID del usuario a eliminar

**Response Exitosa (204 No Content)**: Sin contenido

---

### 1.7. Obtener Perfil Actual

**Endpoint**: `GET /api/v1/usuarios/me/profile`

**Objetivo**: Obtener el perfil del usuario actualmente autenticado.

**Autenticación**: Requerida

**Response Exitosa (200 OK)**:
```json
{
  "id_usuario": 1,
  "login": "juan.perez",
  "correo_electronico": "juan.perez@email.com",
  "estatus_id": 1
}
```

---

### 1.8. Verificar Disponibilidad para Registro

**Endpoint**: `POST /api/v1/usuarios/verificar-disponibilidad`

**Objetivo**: Verificar si un login y correo están disponibles para registro de cliente.

**Autenticación**: No requerida

**Request Body**:
```json
{
  "login": "nuevo.cliente",
  "correo_electronico": "cliente@email.com"
}
```

**Response Exitosa (200 OK)**:
```json
{
  "login_disponible": true,
  "correo_disponible": true,
  "mensaje": "Login y correo disponibles"
}
```

---

### 1.9. Registrar Usuario Cliente

**Endpoint**: `POST /api/v1/usuarios/registro-cliente`

**Objetivo**: Registrar un nuevo usuario asociado a un cliente.

**Autenticación**: No requerida

**Request Body**:
```json
{
  "login": "cliente.nuevo",
  "correo_electronico": "cliente@email.com",
  "password": "Password123",
  "cliente_id": 5
}
```

**Parámetros**:
- `login` (string, requerido): Login del usuario
- `correo_electronico` (string, requerido): Correo (debe coincidir con el del cliente)
- `password` (string, opcional): Contraseña (se genera si no se envía)
- `cliente_id` (integer, requerido): ID del cliente a asociar

**Response Exitosa (201 Created)**:
```json
{
  "id_usuario": 10,
  "login": "cliente.nuevo",
  "correo_electronico": "cliente@email.com",
  "cliente_id": 5,
  "password_temporal": "TempPass123"
}
```

---

### 1.10. Cambiar Contraseña Temporal

**Endpoint**: `POST /api/v1/usuarios/cambiar-password-temporal`

**Objetivo**: Cambiar una contraseña temporal por una definitiva.

**Autenticación**: No requerida

**Request Body**:
```json
{
  "login": "cliente.nuevo",
  "password_actual": "TempPass123",
  "password_nueva": "NuevaPassword123",
  "password_confirmacion": "NuevaPassword123"
}
```

**Response Exitosa (200 OK)**:
```json
{
  "mensaje": "Contraseña actualizada exitosamente",
  "requiere_cambio": false
}
```

---

## 2. Hoteles

### 2.1. Listar Hoteles

**Endpoint**: `GET /api/v1/hotel/`

**Objetivo**: Obtener lista de todos los hoteles con paginación.

**Autenticación**: Requerida

**Query Parameters**:
- `skip` (integer, opcional): Número de registros a saltar (default: 0)
- `limit` (integer, opcional): Número máximo de registros (default: 100, máximo: 1000)

**Response Exitosa (200 OK)**:
```json
[
  {
    "id_hotel": 1,
    "nombre": "Hotel Plaza Madrid",
    "direccion": "Calle Gran Vía, 123, 28013 Madrid",
    "id_pais": 1,
    "id_estado": 15,
    "codigo_postal": "28013",
    "telefono": "+34 91 123 45 67",
    "email_contacto": "reservas@hotelplaza.com",
    "numero_estrellas": 4,
    "url_foto_perfil": "https://innpulse360.supabase.co/storage/v1/object/public/images/hotel/1/1.jpg"
  }
]
```

**Ejemplo cURL**:
```bash
curl -X GET "http://localhost:8000/api/v1/hotel/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 2.2. Obtener Hotel por ID

**Endpoint**: `GET /api/v1/hotel/{hotel_id}`

**Objetivo**: Obtener información de un hotel específico.

**Autenticación**: Requerida

**Path Parameters**:
- `hotel_id` (integer, requerido): ID del hotel

**Response Exitosa (200 OK)**:
```json
{
  "id_hotel": 1,
  "nombre": "Hotel Plaza Madrid",
  "direccion": "Calle Gran Vía, 123, 28013 Madrid",
  "id_pais": 1,
  "id_estado": 15,
  "codigo_postal": "28013",
  "telefono": "+34 91 123 45 67",
  "email_contacto": "reservas@hotelplaza.com",
  "numero_estrellas": 4,
  "url_foto_perfil": "https://innpulse360.supabase.co/storage/v1/object/public/images/hotel/1/1.jpg"
}
```

**Errores Posibles**:
- `404 Not Found`: Hotel no encontrado

---

### 2.3. Crear Hotel

**Endpoint**: `POST /api/v1/hotel/`

**Objetivo**: Crear un nuevo hotel.

**Autenticación**: Requerida

**Request Body**:
```json
{
  "nombre": "Hotel Nuevo",
  "direccion": "Calle Principal 456",
  "id_pais": 1,
  "id_estado": 15,
  "codigo_postal": "28001",
  "telefono": "+34 91 987 65 43",
  "email_contacto": "contacto@hotelnuevo.com",
  "numero_estrellas": 5
}
```

**Parámetros**:
- `nombre` (string, requerido): Nombre del hotel
- `direccion` (string, requerido): Dirección completa
- `id_pais` (integer, requerido): ID del país
- `id_estado` (integer, requerido): ID del estado
- `codigo_postal` (string, opcional): Código postal
- `telefono` (string, opcional): Teléfono de contacto
- `email_contacto` (string, opcional): Email de contacto
- `numero_estrellas` (integer, opcional): Número de estrellas (1-5)

**Response Exitosa (201 Created)**:
```json
{
  "id_hotel": 5,
  "nombre": "Hotel Nuevo",
  "direccion": "Calle Principal 456",
  "id_pais": 1,
  "id_estado": 15,
  "codigo_postal": "28001",
  "telefono": "+34 91 987 65 43",
  "email_contacto": "contacto@hotelnuevo.com",
  "numero_estrellas": 5,
  "url_foto_perfil": null
}
```

---

### 2.4. Actualizar Hotel

**Endpoint**: `PUT /api/v1/hotel/{hotel_id}`

**Objetivo**: Actualizar información de un hotel (actualización parcial).

**Autenticación**: Requerida

**Path Parameters**:
- `hotel_id` (integer, requerido): ID del hotel a actualizar

**Request Body** (todos los campos son opcionales):
```json
{
  "nombre": "Hotel Actualizado",
  "telefono": "+34 91 111 22 33",
  "numero_estrellas": 5
}
```

**Response Exitosa (200 OK)**: Retorna el hotel actualizado

---

### 2.5. Eliminar Hotel

**Endpoint**: `DELETE /api/v1/hotel/{hotel_id}`

**Objetivo**: Eliminar un hotel.

**Autenticación**: Requerida

**Path Parameters**:
- `hotel_id` (integer, requerido): ID del hotel a eliminar

**Response Exitosa (204 No Content)**: Sin contenido

---

### 2.6. Buscar Hoteles por Nombre

**Endpoint**: `GET /api/v1/hotel/buscar/nombre/{nombre}`

**Objetivo**: Buscar hoteles por nombre (búsqueda parcial).

**Autenticación**: Requerida

**Path Parameters**:
- `nombre` (string, requerido): Nombre o parte del nombre a buscar

**Response Exitosa (200 OK)**:
```json
[
  {
    "id_hotel": 1,
    "nombre": "Hotel Plaza Madrid",
    ...
  }
]
```

---

### 2.7. Obtener Hoteles por País

**Endpoint**: `GET /api/v1/hotel/pais/{id_pais}`

**Objetivo**: Obtener todos los hoteles de un país específico.

**Autenticación**: Requerida

**Path Parameters**:
- `id_pais` (integer, requerido): ID del país

**Response Exitosa (200 OK)**: Lista de hoteles del país

---

### 2.8. Obtener Hoteles por Estrellas

**Endpoint**: `GET /api/v1/hotel/estrellas/{numero_estrellas}`

**Objetivo**: Obtener hoteles filtrados por número de estrellas.

**Autenticación**: Requerida

**Path Parameters**:
- `numero_estrellas` (integer, requerido): Número de estrellas (1-5)

**Response Exitosa (200 OK)**: Lista de hoteles con el número de estrellas especificado

**Errores Posibles**:
- `400 Bad Request`: Número de estrellas inválido (debe estar entre 1 y 5)

---

### 2.9. Tipos de Habitación

#### Listar Tipos de Habitación
**Endpoint**: `GET /api/v1/tipos-habitacion/`

**Objetivo**: Obtener lista de todos los tipos de habitación con paginación.

**Autenticación**: Requerida

**Query Parameters**:
- `skip` (integer, opcional): Número de registros a saltar (default: 0)
- `limit` (integer, opcional): Número máximo de registros (default: 100, máximo: 1000)

**Response Exitosa (200 OK)**: Lista de tipos de habitación

---

#### Obtener Tipo de Habitación por ID
**Endpoint**: `GET /api/v1/tipos-habitacion/{id_tipoHabitacion}`

**Objetivo**: Obtener información de un tipo de habitación específico.

**Autenticación**: Requerida

**Path Parameters**:
- `id_tipoHabitacion` (integer, requerido): ID del tipo de habitación

**Errores Posibles**:
- `404 Not Found`: Tipo de habitación no encontrado

---

#### Obtener Tipo de Habitación por Clave
**Endpoint**: `GET /api/v1/tipos-habitacion/clave/{clave}`

**Objetivo**: Obtener un tipo de habitación por su clave.

**Autenticación**: Requerida

**Path Parameters**:
- `clave` (string, requerido): Clave del tipo de habitación

---

#### Obtener Tipo de Habitación por Nombre
**Endpoint**: `GET /api/v1/tipos-habitacion/nombre/{tipo_habitacion}`

**Objetivo**: Obtener un tipo de habitación por su nombre.

**Autenticación**: Requerida

**Path Parameters**:
- `tipo_habitacion` (string, requerido): Nombre del tipo de habitación

---

#### Crear Tipo de Habitación
**Endpoint**: `POST /api/v1/tipos-habitacion/`

**Objetivo**: Crear un nuevo tipo de habitación.

**Autenticación**: Requerida

**Request Body**:
```json
{
  "clave": "SUITE",
  "tipo_habitacion": "Suite Presidencial",
  "estatus_id": 1
}
```

**Parámetros**:
- `clave` (string, opcional): Clave del tipo de habitación
- `tipo_habitacion` (string, requerido): Nombre del tipo de habitación
- `estatus_id` (integer, opcional): Estatus (1=Activo por defecto)

**Response Exitosa (201 Created)**: Objeto TipoHabitacionResponse

---

#### Actualizar Tipo de Habitación
**Endpoint**: `PUT /api/v1/tipos-habitacion/{id_tipoHabitacion}`

**Objetivo**: Actualizar información de un tipo de habitación.

**Autenticación**: Requerida

**Path Parameters**:
- `id_tipoHabitacion` (integer, requerido): ID del tipo de habitación

---

#### Eliminar Tipo de Habitación
**Endpoint**: `DELETE /api/v1/tipos-habitacion/{id_tipoHabitacion}`

**Objetivo**: Eliminar un tipo de habitación (eliminación lógica).

**Autenticación**: Requerida

**Path Parameters**:
- `id_tipoHabitacion` (integer, requerido): ID del tipo de habitación

**Response Exitosa (204 No Content)**: Sin contenido

---

#### Reactivar Tipo de Habitación
**Endpoint**: `PATCH /api/v1/tipos-habitacion/{id_tipoHabitacion}/reactivate`

**Objetivo**: Reactivar un tipo de habitación (cambiar estatus a activo).

**Autenticación**: Requerida

**Path Parameters**:
- `id_tipoHabitacion` (integer, requerido): ID del tipo de habitación

**Response Exitosa (200 OK)**:
```json
{
  "message": "Tipo de habitación reactivado exitosamente"
}
```

---

### 2.10. Características

#### Listar Características
**Endpoint**: `GET /api/v1/caracteristicas/`

**Objetivo**: Obtener lista de todas las características con paginación.

**Autenticación**: Requerida

**Query Parameters**:
- `skip` (integer, opcional): Número de registros a saltar (default: 0)
- `limit` (integer, opcional): Número máximo de registros (default: 100, máximo: 1000)

**Response Exitosa (200 OK)**: Lista de características

---

#### Obtener Característica por ID
**Endpoint**: `GET /api/v1/caracteristicas/{id_caracteristica}`

**Objetivo**: Obtener información de una característica específica.

**Autenticación**: Requerida

**Path Parameters**:
- `id_caracteristica` (integer, requerido): ID de la característica

**Errores Posibles**:
- `404 Not Found`: Característica no encontrada

---

#### Obtener Característica por Nombre
**Endpoint**: `GET /api/v1/caracteristicas/nombre/{caracteristica}`

**Objetivo**: Obtener una característica por su nombre.

**Autenticación**: Requerida

**Path Parameters**:
- `caracteristica` (string, requerido): Nombre de la característica

---

#### Crear Característica
**Endpoint**: `POST /api/v1/caracteristicas/`

**Objetivo**: Crear una nueva característica.

**Autenticación**: Requerida

**Request Body**:
```json
{
  "caracteristica": "WiFi Gratis",
  "descripcion": "Conexión WiFi gratuita de alta velocidad"
}
```

**Parámetros**:
- `caracteristica` (string, requerido): Nombre de la característica
- `descripcion` (string, opcional): Descripción de la característica

**Response Exitosa (201 Created)**: Objeto CaracteristicaResponse

---

#### Actualizar Característica
**Endpoint**: `PUT /api/v1/caracteristicas/{id_caracteristica}`

**Objetivo**: Actualizar información de una característica.

**Autenticación**: Requerida

**Path Parameters**:
- `id_caracteristica` (integer, requerido): ID de la característica

---

#### Eliminar Característica
**Endpoint**: `DELETE /api/v1/caracteristicas/{id_caracteristica}`

**Objetivo**: Eliminar una característica.

**Autenticación**: Requerida

**Path Parameters**:
- `id_caracteristica` (integer, requerido): ID de la característica

**Response Exitosa (204 No Content)**: Sin contenido

---

### 2.11. Tipo Habitación-Característica

#### Asignar Característica a Tipo de Habitación
**Endpoint**: `POST /api/v1/tipos-habitacion/{tipo_habitacion_id}/caracteristicas/{caracteristica_id}`

**Objetivo**: Asignar una característica a un tipo de habitación.

**Autenticación**: Requerida

**Path Parameters**:
- `tipo_habitacion_id` (integer, requerido): ID del tipo de habitación
- `caracteristica_id` (integer, requerido): ID de la característica

**Response Exitosa (201 Created)**:
```json
{
  "message": "Característica asignada exitosamente al tipo de habitación"
}
```

---

#### Remover Característica de Tipo de Habitación
**Endpoint**: `DELETE /api/v1/tipos-habitacion/{tipo_habitacion_id}/caracteristicas/{caracteristica_id}`

**Objetivo**: Remover una característica de un tipo de habitación.

**Autenticación**: Requerida

**Path Parameters**:
- `tipo_habitacion_id` (integer, requerido): ID del tipo de habitación
- `caracteristica_id` (integer, requerido): ID de la característica

**Response Exitosa (204 No Content)**: Sin contenido

**Errores Posibles**:
- `404 Not Found`: Asignación no encontrada

---

#### Obtener Características de un Tipo de Habitación
**Endpoint**: `GET /api/v1/tipos-habitacion/{tipo_habitacion_id}/caracteristicas`

**Objetivo**: Obtener todas las características asignadas a un tipo de habitación.

**Autenticación**: Requerida

**Path Parameters**:
- `tipo_habitacion_id` (integer, requerido): ID del tipo de habitación

**Response Exitosa (200 OK)**: Lista de características del tipo de habitación

---

#### Asignar Múltiples Características a Tipo de Habitación
**Endpoint**: `PUT /api/v1/tipos-habitacion/{tipo_habitacion_id}/caracteristicas`

**Objetivo**: Asignar múltiples características a un tipo de habitación de una vez.

**Autenticación**: Requerida

**Path Parameters**:
- `tipo_habitacion_id` (integer, requerido): ID del tipo de habitación

**Request Body**:
```json
{
  "caracteristicas_ids": [1, 2, 3, 5]
}
```

**Response Exitosa (200 OK)**:
```json
{
  "message": "Se asignaron 4 características exitosamente",
  "assigned_count": 4,
  "total_requested": 4
}
```

---

#### Remover Múltiples Características de Tipo de Habitación
**Endpoint**: `DELETE /api/v1/tipos-habitacion/{tipo_habitacion_id}/caracteristicas`

**Objetivo**: Remover múltiples características de un tipo de habitación de una vez.

**Autenticación**: Requerida

**Path Parameters**:
- `tipo_habitacion_id` (integer, requerido): ID del tipo de habitación

**Request Body**:
```json
{
  "caracteristicas_ids": [1, 2]
}
```

**Response Exitosa (200 OK)**:
```json
{
  "message": "Se removieron 2 características exitosamente",
  "removed_count": 2,
  "total_requested": 2
}
```

---

#### Obtener Tipos de Habitación por Característica
**Endpoint**: `GET /api/v1/tipos-habitacion/caracteristicas/{caracteristica_id}/tipos-habitacion`

**Objetivo**: Obtener todos los tipos de habitación que tienen una característica específica.

**Autenticación**: Requerida

**Path Parameters**:
- `caracteristica_id` (integer, requerido): ID de la característica

**Response Exitosa (200 OK)**: Lista de tipos de habitación con esa característica

---

### 2.12. Pisos

#### Listar Pisos por Hotel
**Endpoint**: `GET /api/v1/pisos/get-by-hotel/{id_hotel}`

**Objetivo**: Obtener todos los pisos de un hotel específico.

**Autenticación**: No requerida (según código)

**Path Parameters**:
- `id_hotel` (integer, requerido): ID del hotel

**Response Exitosa (200 OK)**: Lista de pisos del hotel

---

#### Obtener Piso por ID
**Endpoint**: `GET /api/v1/pisos/{id_piso}`

**Objetivo**: Obtener información de un piso específico.

**Autenticación**: No requerida (según código)

**Path Parameters**:
- `id_piso` (integer, requerido): ID del piso

**Errores Posibles**:
- `404 Not Found`: Piso no encontrado

---

#### Crear Piso
**Endpoint**: `POST /api/v1/pisos/`

**Objetivo**: Crear un nuevo piso.

**Autenticación**: Requerida

**Request Body**:
```json
{
  "id_hotel": 1,
  "numero_piso": 3,
  "descripcion": "Tercer piso"
}
```

**Response Exitosa (201 Created)**: Objeto PisoResponse

---

#### Actualizar Piso
**Endpoint**: `PUT /api/v1/pisos/{id_piso}`

**Objetivo**: Actualizar información de un piso.

**Autenticación**: Requerida

**Path Parameters**:
- `id_piso` (integer, requerido): ID del piso

**Errores Posibles**:
- `404 Not Found`: Piso no encontrado

---

#### Eliminar Piso
**Endpoint**: `DELETE /api/v1/pisos/{id_piso}`

**Objetivo**: Eliminar un piso.

**Autenticación**: Requerida

**Path Parameters**:
- `id_piso` (integer, requerido): ID del piso

**Response Exitosa (204 No Content)**: Sin contenido

---

### 2.13. Habitación Área

#### Listar Habitaciones por Piso
**Endpoint**: `GET /api/v1/habitacion-area/obtener-por-piso/{piso_id}`

**Objetivo**: Obtener todas las habitaciones de un piso específico.

**Autenticación**: No requerida (según código)

**Path Parameters**:
- `piso_id` (integer, requerido): ID del piso

**Response Exitosa (200 OK)**: Lista de habitaciones del piso

---

#### Obtener Habitación por ID
**Endpoint**: `GET /api/v1/habitacion-area/{id_habitacion_area}`

**Objetivo**: Obtener información de una habitación específica.

**Autenticación**: No requerida (según código)

**Path Parameters**:
- `id_habitacion_area` (integer, requerido): ID de la habitación

**Errores Posibles**:
- `404 Not Found`: Habitación no encontrada

---

#### Crear Habitación
**Endpoint**: `POST /api/v1/habitacion-area/`

**Objetivo**: Crear una nueva habitación.

**Autenticación**: Requerida

**Request Body**:
```json
{
  "id_piso": 1,
  "id_tipo_habitacion": 2,
  "numero_habitacion": "301",
  "descripcion": "Habitación con vista al mar"
}
```

**Response Exitosa (200 OK)**: Objeto HabitacionAreaResponse

---

#### Actualizar Habitación
**Endpoint**: `PUT /api/v1/habitacion-area/{id_habitacion_area}`

**Objetivo**: Actualizar información de una habitación.

**Autenticación**: Requerida

**Path Parameters**:
- `id_habitacion_area` (integer, requerido): ID de la habitación

**Errores Posibles**:
- `404 Not Found`: Habitación no encontrada

---

#### Eliminar Habitación
**Endpoint**: `POST /api/v1/habitacion-area/{id_habitacion_area}`

**Objetivo**: Eliminar una habitación.

**Autenticación**: Requerida

**Path Parameters**:
- `id_habitacion_area` (integer, requerido): ID de la habitación

**Response Exitosa (200 OK)**:
```json
{
  "message": "Habitación eliminada correctamente"
}
```

**Nota**: Este endpoint usa POST en lugar de DELETE según el código.

---

## 3. Clientes

### 3.1. Crear Cliente

**Endpoint**: `POST /api/v1/clientes/`

**Objetivo**: Crear un nuevo cliente en el sistema.

**Autenticación**: Requerida

**Request Body**:
```json
{
  "tipo_persona": 1,
  "documento_identificacion": 123456789,
  "nombre_razon_social": "Juan Pérez González",
  "apellido_paterno": "Pérez",
  "apellido_materno": "González",
  "rfc": "PEGJ800101XXX",
  "curp": "PEGJ800101HDFRRN01",
  "telefono": "5512345678",
  "direccion": "Calle Principal 123, Col. Centro",
  "pais_id": 1,
  "estado_id": 15,
  "correo_electronico": "cliente@email.com",
  "representante": "Juan Pérez",
  "id_estatus": 1
}
```

**Parámetros**:
- `tipo_persona` (integer, requerido): 1=Persona Física, 2=Persona Moral
- `documento_identificacion` (integer, requerido): Número de identificación
- `nombre_razon_social` (string, requerido): Nombre completo o Razón Social
- `apellido_paterno` (string, opcional): Apellido paterno
- `apellido_materno` (string, opcional): Apellido materno
- `rfc` (string, opcional): RFC (12-13 caracteres, único)
- `curp` (string, opcional): CURP (18 caracteres)
- `telefono` (string, opcional): Teléfono
- `direccion` (string, opcional): Dirección
- `pais_id` (integer, requerido): ID del país
- `estado_id` (integer, requerido): ID del estado
- `correo_electronico` (string, requerido): Email del cliente
- `representante` (string, requerido): Nombre del representante
- `id_estatus` (integer, opcional): Estatus (1=Activo, 0=Inactivo, default: 1)

**Response Exitosa (201 Created)**:
```json
{
  "id_cliente": 1,
  "tipo_persona": 1,
  "documento_identificacion": 123456789,
  "nombre_razon_social": "Juan Pérez González",
  "apellido_paterno": "Pérez",
  "apellido_materno": "González",
  "rfc": "PEGJ800101XXX",
  "curp": "PEGJ800101HDFRRN01",
  "telefono": "5512345678",
  "direccion": "Calle Principal 123, Col. Centro",
  "pais_id": 1,
  "estado_id": 15,
  "correo_electronico": "cliente@email.com",
  "representante": "Juan Pérez",
  "id_estatus": 1
}
```

**Errores Posibles**:
- `400 Bad Request`: RFC duplicado o datos inválidos

---

### 3.2. Listar Clientes

**Endpoint**: `GET /api/v1/clientes/`

**Objetivo**: Obtener lista de todos los clientes con paginación.

**Autenticación**: Requerida

**Query Parameters**:
- `skip` (integer, opcional): Número de registros a saltar (default: 0)
- `limit` (integer, opcional): Número máximo de registros (default: 100, máximo: 1000)

**Response Exitosa (200 OK)**: Lista de clientes

---

### 3.3. Obtener Clientes Activos

**Endpoint**: `GET /api/v1/clientes/activos`

**Objetivo**: Obtener solo los clientes con estatus activo.

**Autenticación**: Requerida

**Query Parameters**:
- `skip` (integer, opcional): Número de registros a saltar
- `limit` (integer, opcional): Número máximo de registros

---

### 3.4. Obtener Cliente por ID

**Endpoint**: `GET /api/v1/clientes/{cliente_id}`

**Objetivo**: Obtener información de un cliente específico.

**Autenticación**: Requerida

**Path Parameters**:
- `cliente_id` (integer, requerido): ID del cliente

**Response Exitosa (200 OK)**: Objeto ClienteResponse

**Errores Posibles**:
- `404 Not Found`: Cliente no encontrado

---

### 3.5. Actualizar Cliente

**Endpoint**: `PUT /api/v1/clientes/{cliente_id}`

**Objetivo**: Actualizar información de un cliente (actualización parcial).

**Autenticación**: Requerida

**Path Parameters**:
- `cliente_id` (integer, requerido): ID del cliente

**Request Body** (todos los campos son opcionales):
```json
{
  "telefono": "5598765432",
  "direccion": "Nueva Dirección 456"
}
```

**Nota**: Si se actualiza el RFC, se valida que no exista duplicado.

---

### 3.6. Eliminar Cliente

**Endpoint**: `DELETE /api/v1/clientes/{cliente_id}`

**Objetivo**: Eliminar un cliente (soft delete - cambia estatus a inactivo).

**Autenticación**: Requerida

**Path Parameters**:
- `cliente_id` (integer, requerido): ID del cliente

**Response Exitosa (204 No Content)**: Sin contenido

---

### 3.7. Buscar Cliente por RFC

**Endpoint**: `GET /api/v1/clientes/buscar/rfc/{rfc}`

**Objetivo**: Buscar un cliente por su RFC.

**Autenticación**: Requerida

**Path Parameters**:
- `rfc` (string, requerido): RFC del cliente

**Response Exitosa (200 OK)**: Objeto ClienteResponse

**Errores Posibles**:
- `404 Not Found`: Cliente no encontrado

---

### 3.8. Verificar RFC Disponible

**Endpoint**: `GET /api/v1/clientes/verificar-rfc/{rfc}`

**Objetivo**: Verificar si un RFC está disponible (no existe en la base de datos).

**Autenticación**: Requerida

**Path Parameters**:
- `rfc` (string, requerido): RFC a verificar

**Response Exitosa (200 OK)**:
```json
{
  "rfc": "PEGJ800101XXX",
  "disponible": true,
  "mensaje": "RFC disponible"
}
```

---

### 3.9. Buscar Clientes por Nombre

**Endpoint**: `GET /api/v1/clientes/buscar/nombre?nombre={nombre}`

**Objetivo**: Buscar clientes por nombre o razón social (búsqueda parcial).

**Autenticación**: Requerida

**Query Parameters**:
- `nombre` (string, requerido): Texto a buscar en nombre/razón social
- `skip` (integer, opcional): Número de registros a saltar
- `limit` (integer, opcional): Número máximo de registros

**Response Exitosa (200 OK)**: Lista de clientes encontrados

---

### 3.10. Obtener Clientes por Tipo de Persona

**Endpoint**: `GET /api/v1/clientes/tipo-persona/{tipo_persona}`

**Objetivo**: Obtener clientes filtrados por tipo de persona.

**Autenticación**: Requerida

**Path Parameters**:
- `tipo_persona` (integer, requerido): 1=Persona Física, 2=Persona Moral

**Query Parameters**:
- `skip` (integer, opcional): Número de registros a saltar
- `limit` (integer, opcional): Número máximo de registros

**Errores Posibles**:
- `400 Bad Request`: Tipo de persona debe ser 1 o 2

---

## 4. Reservaciones

### 4.1. Tipos de Cargo

#### Listar Tipos de Cargo
**Endpoint**: `GET /api/v1/tipos-cargo/`

**Objetivo**: Obtener lista de todos los tipos de cargo disponibles.

**Autenticación**: Requerida

**Response Exitosa (200 OK)**: Lista de tipos de cargo

---

#### Obtener Tipo de Cargo por ID
**Endpoint**: `GET /api/v1/tipos-cargo/{id_tipo}`

**Objetivo**: Obtener información de un tipo de cargo específico.

**Autenticación**: Requerida

**Path Parameters**:
- `id_tipo` (integer, requerido): ID del tipo de cargo

**Errores Posibles**:
- `404 Not Found`: Tipo de cargo no encontrado

---

#### Crear Tipo de Cargo
**Endpoint**: `POST /api/v1/tipos-cargo/`

**Objetivo**: Crear un nuevo tipo de cargo.

**Autenticación**: Requerida

**Request Body**:
```json
{
  "tipo_cargo": "Desayuno",
  "descripcion": "Servicio de desayuno incluido"
}
```

**Response Exitosa (201 Created)**: Objeto TipoCargoResponse

---

#### Actualizar Tipo de Cargo
**Endpoint**: `PUT /api/v1/tipos-cargo/{id_tipo}`

**Objetivo**: Actualizar información de un tipo de cargo.

**Autenticación**: Requerida

**Path Parameters**:
- `id_tipo` (integer, requerido): ID del tipo de cargo

---

#### Eliminar Tipo de Cargo
**Endpoint**: `DELETE /api/v1/tipos-cargo/{id_tipo}`

**Objetivo**: Eliminar un tipo de cargo.

**Autenticación**: Requerida

**Path Parameters**:
- `id_tipo` (integer, requerido): ID del tipo de cargo

**Response Exitosa (204 No Content)**: Sin contenido

---

### 4.2. Cargos

#### Listar Cargos
**Endpoint**: `GET /api/v1/cargos/`

**Objetivo**: Obtener lista de todos los cargos.

**Autenticación**: Requerida

**Response Exitosa (200 OK)**: Lista de cargos

---

#### Obtener Cargo por ID
**Endpoint**: `GET /api/v1/cargos/{id_cargo}`

**Objetivo**: Obtener información de un cargo específico.

**Autenticación**: Requerida

**Path Parameters**:
- `id_cargo` (integer, requerido): ID del cargo

**Errores Posibles**:
- `404 Not Found`: Cargo no encontrado

---

#### Obtener Cargos por Reservación
**Endpoint**: `GET /api/v1/cargos/get-by-reserva/{id_reserva}`

**Objetivo**: Obtener todos los cargos asociados a una reservación.

**Autenticación**: Requerida

**Path Parameters**:
- `id_reserva` (integer, requerido): ID de la reservación

**Response Exitosa (200 OK)**: Lista de cargos de la reservación

---

#### Crear Cargo
**Endpoint**: `POST /api/v1/cargos/`

**Objetivo**: Crear un nuevo cargo.

**Autenticación**: Requerida

**Request Body**:
```json
{
  "id_reservacion": 1,
  "id_tipo_cargo": 1,
  "cantidad": 2,
  "precio_unitario": 150.00,
  "descripcion": "Desayuno para 2 personas"
}
```

**Response Exitosa (201 Created)**: Objeto CargoResponse

---

#### Crear Cargo con Servicio de Transporte
**Endpoint**: `POST /api/v1/cargos/create-cargo-servicio-transporte?servicio_transporte_id={servicio_transporte_id}`

**Objetivo**: Crear un cargo y asociarlo automáticamente con un servicio de transporte.

**Autenticación**: Requerida

**Query Parameters**:
- `servicio_transporte_id` (integer, requerido): ID del servicio de transporte

**Request Body**: Mismo que crear cargo

**Response Exitosa (201 Created)**: Objeto CargoResponse con servicio de transporte asociado

---

#### Actualizar Cargo
**Endpoint**: `PUT /api/v1/cargos/{id_cargo}`

**Objetivo**: Actualizar información de un cargo.

**Autenticación**: Requerida

**Path Parameters**:
- `id_cargo` (integer, requerido): ID del cargo

---

#### Eliminar Cargo
**Endpoint**: `DELETE /api/v1/cargos/{id_cargo}`

**Objetivo**: Eliminar un cargo.

**Autenticación**: Requerida

**Path Parameters**:
- `id_cargo` (integer, requerido): ID del cargo

**Response Exitosa (204 No Content)**: Sin contenido

---

### 4.3. Servicios de Transporte

#### Listar Servicios de Transporte
**Endpoint**: `GET /api/v1/servicios-transporte/`

**Objetivo**: Obtener lista de todos los servicios de transporte disponibles.

**Autenticación**: Requerida

**Response Exitosa (200 OK)**: Lista de servicios de transporte

---

#### Obtener Servicio de Transporte por ID
**Endpoint**: `GET /api/v1/servicios-transporte/{id_servicio}`

**Objetivo**: Obtener información de un servicio de transporte específico.

**Autenticación**: Requerida

**Path Parameters**:
- `id_servicio` (integer, requerido): ID del servicio

**Errores Posibles**:
- `404 Not Found`: Servicio no encontrado

---

#### Crear Servicio de Transporte
**Endpoint**: `POST /api/v1/servicios-transporte/`

**Objetivo**: Crear un nuevo servicio de transporte.

**Autenticación**: Requerida

**Request Body**:
```json
{
  "nombre": "Transporte Aeropuerto",
  "descripcion": "Servicio de transporte desde/hacia el aeropuerto",
  "precio": 500.00
}
```

**Response Exitosa (200 OK)**: Objeto ServicioTransporteResponse

---

#### Actualizar Servicio de Transporte
**Endpoint**: `PUT /api/v1/servicios-transporte/{id_servicio}`

**Objetivo**: Actualizar información de un servicio de transporte.

**Autenticación**: Requerida

**Path Parameters**:
- `id_servicio` (integer, requerido): ID del servicio

---

#### Eliminar Servicio de Transporte
**Endpoint**: `DELETE /api/v1/servicios-transporte/{id_servicio}`

**Objetivo**: Eliminar un servicio de transporte.

**Autenticación**: Requerida

**Path Parameters**:
- `id_servicio` (integer, requerido): ID del servicio

**Response Exitosa (200 OK)**:
```json
{
  "message": "Servicio eliminado correctamente"
}
```

---

### 4.4. Cargo-Servicio Transporte

#### Listar Relaciones Cargo-Servicio Transporte
**Endpoint**: `GET /api/v1/cargo-servicio-transporte/`

**Objetivo**: Obtener lista de todas las relaciones entre cargos y servicios de transporte.

**Autenticación**: Requerida

**Response Exitosa (200 OK)**: Lista de relaciones

---

#### Obtener Relaciones por Cargo
**Endpoint**: `GET /api/v1/cargo-servicio-transporte/cargo/{cargo_id}`

**Objetivo**: Obtener todos los servicios de transporte asociados a un cargo.

**Autenticación**: Requerida

**Path Parameters**:
- `cargo_id` (integer, requerido): ID del cargo

**Response Exitosa (200 OK)**: Lista de relaciones del cargo

---

#### Obtener Relaciones por Servicio
**Endpoint**: `GET /api/v1/cargo-servicio-transporte/servicio/{servicio_id}`

**Objetivo**: Obtener todos los cargos asociados a un servicio de transporte.

**Autenticación**: Requerida

**Path Parameters**:
- `servicio_id` (integer, requerido): ID del servicio de transporte

**Response Exitosa (200 OK)**: Lista de relaciones del servicio

---

#### Eliminar Relación Cargo-Servicio Transporte
**Endpoint**: `DELETE /api/v1/cargo-servicio-transporte/?cargo_id={cargo_id}&servicio_id={servicio_id}`

**Objetivo**: Eliminar la relación entre un cargo y un servicio de transporte.

**Autenticación**: Requerida

**Query Parameters**:
- `cargo_id` (integer, requerido): ID del cargo
- `servicio_id` (integer, requerido): ID del servicio de transporte

**Response Exitosa (200 OK)**: Objeto CargoServicioTransporteResponse eliminado

**Errores Posibles**:
- `404 Not Found`: Relación no encontrada

---

### 4.5. Listar Reservaciones

**Endpoint**: `GET /api/v1/reservaciones/`

**Objetivo**: Obtener lista de todas las reservaciones.

**Autenticación**: Requerida

**Response Exitosa (200 OK)**:
```json
[
  {
    "id_reservacion": 1,
    "id_cliente": 5,
    "habitacion_area_id": 10,
    "fecha_entrada": "2024-12-01T14:00:00",
    "fecha_salida": "2024-12-05T12:00:00",
    "numero_huespedes": 2,
    "estatus_id": 1
  }
]
```

---

### 4.2. Obtener Reservación por ID

**Endpoint**: `GET /api/v1/reservaciones/{id_reservacion}`

**Objetivo**: Obtener información de una reservación específica.

**Autenticación**: Requerida

**Path Parameters**:
- `id_reservacion` (integer, requerido): ID de la reservación

**Errores Posibles**:
- `404 Not Found`: Reservación no encontrada

---

### 4.3. Obtener Reservaciones por Cliente

**Endpoint**: `GET /api/v1/reservaciones/cliente/{id_cliente}`

**Objetivo**: Obtener todas las reservaciones de un cliente específico.

**Autenticación**: Requerida

**Path Parameters**:
- `id_cliente` (integer, requerido): ID del cliente

**Response Exitosa (200 OK)**: Lista de reservaciones del cliente

---

### 4.4. Obtener Reservaciones por Habitación

**Endpoint**: `GET /api/v1/reservaciones/habitacion/{habitacion_area_id}`

**Objetivo**: Obtener todas las reservaciones de una habitación específica.

**Autenticación**: Requerida

**Path Parameters**:
- `habitacion_area_id` (integer, requerido): ID de la habitación

---

### 4.5. Obtener Reservaciones por Fechas

**Endpoint**: `GET /api/v1/reservaciones/fechas/?fecha_inicio={fecha_inicio}&fecha_fin={fecha_fin}`

**Objetivo**: Obtener reservaciones en un rango de fechas.

**Autenticación**: Requerida

**Query Parameters**:
- `fecha_inicio` (datetime, requerido): Fecha inicial (formato: YYYY-MM-DDTHH:MM:SS)
- `fecha_fin` (datetime, requerido): Fecha final (formato: YYYY-MM-DDTHH:MM:SS)

**Ejemplo**:
```
GET /api/v1/reservaciones/fechas/?fecha_inicio=2024-12-01T00:00:00&fecha_fin=2024-12-31T23:59:59
```

---

### 4.6. Crear Reservación

**Endpoint**: `POST /api/v1/reservaciones/`

**Objetivo**: Crear una nueva reservación.

**Autenticación**: Requerida

**Request Body**:
```json
{
  "id_cliente": 5,
  "habitacion_area_id": 10,
  "fecha_entrada": "2024-12-01T14:00:00",
  "fecha_salida": "2024-12-05T12:00:00",
  "numero_huespedes": 2,
  "estatus_id": 1
}
```

**Response Exitosa (200 OK)**: Objeto ReservacionResponse con el ID generado

---

### 4.7. Actualizar Reservación

**Endpoint**: `PUT /api/v1/reservaciones/{id_reservacion}`

**Objetivo**: Actualizar información de una reservación.

**Autenticación**: Requerida

**Path Parameters**:
- `id_reservacion` (integer, requerido): ID de la reservación

**Request Body** (todos los campos son opcionales):
```json
{
  "numero_huespedes": 3,
  "fecha_salida": "2024-12-06T12:00:00"
}
```

**Errores Posibles**:
- `404 Not Found`: Reservación no encontrada

---

### 4.8. Eliminar Reservación

**Endpoint**: `DELETE /api/v1/reservaciones/{id_reservacion}`

**Objetivo**: Eliminar una reservación.

**Autenticación**: Requerida

**Path Parameters**:
- `id_reservacion` (integer, requerido): ID de la reservación

**Response Exitosa (200 OK)**: Objeto ReservacionResponse eliminado

**Errores Posibles**:
- `404 Not Found`: Reservación no encontrada

---

## 5. Empleados

### 5.1. Crear Empleado

**Endpoint**: `POST /api/v1/empleado/`

**Objetivo**: Crear un nuevo empleado en el sistema.

**Autenticación**: Requerida

**Request Body**:
```json
{
  "nombre": "Juan",
  "apellido_paterno": "Pérez",
  "apellido_materno": "González",
  "telefono": "5512345678",
  "email": "juan.perez@hotel.com",
  "id_puesto": 1,
  "id_hotel": 1,
  "direccion": {
    "calle": "Calle Principal 123",
    "colonia": "Centro",
    "codigo_postal": "28001",
    "id_pais": 1,
    "id_estado": 15
  }
}
```

**Response Exitosa (201 Created)**: Objeto EmpleadoResponse

---

### 5.2. Obtener Empleados por Hotel

**Endpoint**: `GET /api/v1/empleado/empleado-hotel/{hotel_id}`

**Objetivo**: Obtener todos los empleados de un hotel específico.

**Autenticación**: Requerida

**Path Parameters**:
- `hotel_id` (integer, requerido): ID del hotel

**Query Parameters**:
- `skip` (integer, opcional): Número de registros a saltar (default: 0)
- `limit` (integer, opcional): Número máximo de registros (default: 100, máximo: 1000)

**Response Exitosa (200 OK)**: Lista de empleados del hotel

---

### 5.3. Obtener Empleado por ID

**Endpoint**: `GET /api/v1/empleado/{empleado_id}`

**Objetivo**: Obtener información de un empleado específico.

**Autenticación**: Requerida

**Path Parameters**:
- `empleado_id` (integer, requerido): ID del empleado

**Errores Posibles**:
- `404 Not Found`: Empleado no encontrado

---

### 5.4. Actualizar Empleado

**Endpoint**: `PUT /api/v1/empleado/{empleado_id}`

**Objetivo**: Actualizar información de un empleado.

**Autenticación**: Requerida

**Path Parameters**:
- `empleado_id` (integer, requerido): ID del empleado

**Request Body** (todos los campos son opcionales):
```json
{
  "telefono": "5598765432",
  "email": "nuevo.email@hotel.com"
}
```

---

### 5.5. Eliminar Empleado

**Endpoint**: `DELETE /api/v1/empleado/{empleado_id}`

**Objetivo**: Eliminar un empleado físicamente de la base de datos.

**Autenticación**: Requerida

**Path Parameters**:
- `empleado_id` (integer, requerido): ID del empleado

**Response Exitosa (204 No Content)**: Sin contenido

---

### 5.6. Actualizar Dirección de Empleado

**Endpoint**: `PUT /api/v1/empleado/editar-direccion/{direccion_id}`

**Objetivo**: Actualizar la dirección de un empleado.

**Autenticación**: Requerida

**Path Parameters**:
- `direccion_id` (integer, requerido): ID de la dirección

**Request Body**:
```json
{
  "calle": "Nueva Calle 456",
  "colonia": "Nueva Colonia",
  "codigo_postal": "28002"
}
```

---

## 6. Limpieza (Camarista)

### 6.1. Listar Limpiezas

**Endpoint**: `GET /api/v1/limpiezas/`

**Objetivo**: Obtener lista de todas las limpiezas.

**Autenticación**: Requerida

**Response Exitosa (200 OK)**: Lista de limpiezas

---

### 6.2. Obtener Limpieza por ID

**Endpoint**: `GET /api/v1/limpiezas/{id_limpieza}`

**Objetivo**: Obtener información de una limpieza específica.

**Autenticación**: Requerida

**Path Parameters**:
- `id_limpieza` (integer, requerido): ID de la limpieza

**Errores Posibles**:
- `404 Not Found`: Limpieza no encontrada o eliminada

---

### 6.3. Crear Limpieza

**Endpoint**: `POST /api/v1/limpiezas/`

**Objetivo**: Crear una nueva limpieza.

**Autenticación**: Requerida

**Request Body**:
```json
{
  "habitacion_area_id": 10,
  "empleado_id": 5,
  "tipo_limpieza_id": 1,
  "estatus_limpieza_id": 1,
  "fecha_limpieza": "2024-12-01T10:00:00",
  "observaciones": "Limpieza completa realizada"
}
```

---

### 6.4. Actualizar Limpieza

**Endpoint**: `PUT /api/v1/limpiezas/{id_limpieza}`

**Objetivo**: Actualizar información de una limpieza.

**Autenticación**: Requerida

**Path Parameters**:
- `id_limpieza` (integer, requerido): ID de la limpieza

**Errores Posibles**:
- `404 Not Found`: Limpieza no encontrada o eliminada

---

### 6.5. Eliminar Limpieza

**Endpoint**: `DELETE /api/v1/limpiezas/{id_limpieza}`

**Objetivo**: Eliminar una limpieza (marcar como eliminada, estatus_id = 4).

**Autenticación**: Requerida

**Path Parameters**:
- `id_limpieza` (integer, requerido): ID de la limpieza

**Response Exitosa (200 OK)**:
```json
{
  "message": "Limpieza marcada como eliminada (estatus_limpieza_id = 4)"
}
```

**Nota**: Es una eliminación lógica, no física.

---

### 6.6. Obtener Limpiezas por Empleado

**Endpoint**: `GET /api/v1/limpiezas/empleado/{empleado_id}`

**Objetivo**: Obtener todas las limpiezas asignadas a un empleado.

**Autenticación**: Requerida

**Path Parameters**:
- `empleado_id` (integer, requerido): ID del empleado

**Response Exitosa (200 OK)**: Lista de limpiezas del empleado

---

### 6.7. Obtener Limpiezas por Habitación

**Endpoint**: `GET /api/v1/limpiezas/habitacion-area/{habitacion_area_id}`

**Objetivo**: Obtener todas las limpiezas de una habitación específica.

**Autenticación**: Requerida

**Path Parameters**:
- `habitacion_area_id` (integer, requerido): ID de la habitación

---

### 6.8. Obtener Limpiezas por Fecha

**Endpoint**: `GET /api/v1/limpiezas/fecha/?fecha={fecha}`

**Objetivo**: Obtener limpiezas de una fecha específica.

**Autenticación**: Requerida

**Query Parameters**:
- `fecha` (datetime, requerido): Fecha de limpieza (formato: YYYY-MM-DDTHH:MM:SS)

**Ejemplo**:
```
GET /api/v1/limpiezas/fecha/?fecha=2024-12-01T00:00:00
```

---

### 6.9. Tipos de Limpieza

#### Listar Tipos de Limpieza
**Endpoint**: `GET /api/v1/tipos-limpieza/`

**Objetivo**: Obtener lista de todos los tipos de limpieza disponibles.

**Autenticación**: Requerida

**Response Exitosa (200 OK)**: Lista de tipos de limpieza

---

#### Obtener Tipo de Limpieza por ID
**Endpoint**: `GET /api/v1/tipos-limpieza/{id_tipo_limpieza}`

**Objetivo**: Obtener información de un tipo de limpieza específico.

**Autenticación**: Requerida

**Path Parameters**:
- `id_tipo_limpieza` (integer, requerido): ID del tipo de limpieza

**Errores Posibles**:
- `404 Not Found`: Tipo de limpieza no encontrado

---

#### Crear Tipo de Limpieza
**Endpoint**: `POST /api/v1/tipos-limpieza/`

**Objetivo**: Crear un nuevo tipo de limpieza.

**Autenticación**: Requerida

**Request Body**:
```json
{
  "tipo_limpieza": "Limpieza Profunda",
  "descripcion": "Limpieza completa y detallada"
}
```

**Response Exitosa (201 Created)**:
```json
{
  "mensaje": "Tipo de limpieza creado correctamente",
  "data": { ... }
}
```

---

#### Actualizar Tipo de Limpieza
**Endpoint**: `PUT /api/v1/tipos-limpieza/{id_tipo_limpieza}`

**Objetivo**: Actualizar información de un tipo de limpieza.

**Autenticación**: Requerida

**Path Parameters**:
- `id_tipo_limpieza` (integer, requerido): ID del tipo de limpieza

**Response Exitosa (200 OK)**:
```json
{
  "mensaje": "Tipo de limpieza actualizado correctamente",
  "data": { ... }
}
```

**Errores Posibles**:
- `404 Not Found`: Tipo de limpieza no encontrado

---

#### Eliminar Tipo de Limpieza
**Endpoint**: `DELETE /api/v1/tipos-limpieza/{id_tipo_limpieza}`

**Objetivo**: Eliminar un tipo de limpieza.

**Autenticación**: Requerida

**Path Parameters**:
- `id_tipo_limpieza` (integer, requerido): ID del tipo de limpieza

**Response Exitosa (204 No Content)**: Sin contenido

**Errores Posibles**:
- `404 Not Found`: Tipo de limpieza no encontrado

---

### 6.10. Estatus de Limpieza

#### Listar Estatus de Limpieza
**Endpoint**: `GET /api/v1/estatus-limpieza/`

**Objetivo**: Obtener lista de todos los estatus de limpieza disponibles.

**Autenticación**: Requerida

**Response Exitosa (200 OK)**: Lista de estatus de limpieza

---

#### Obtener Estatus de Limpieza por ID
**Endpoint**: `GET /api/v1/estatus-limpieza/{id_estatus_limpieza}`

**Objetivo**: Obtener información de un estatus de limpieza específico.

**Autenticación**: Requerida

**Path Parameters**:
- `id_estatus_limpieza` (integer, requerido): ID del estatus

**Errores Posibles**:
- `404 Not Found`: Estatus no encontrado

---

#### Crear Estatus de Limpieza
**Endpoint**: `POST /api/v1/estatus-limpieza/`

**Objetivo**: Crear un nuevo estatus de limpieza.

**Autenticación**: Requerida

**Request Body**:
```json
{
  "estatus_limpieza": "Completada",
  "descripcion": "Limpieza completada exitosamente"
}
```

**Response Exitosa (201 Created)**: Objeto EstatusLimpiezaResponse

---

#### Actualizar Estatus de Limpieza
**Endpoint**: `PUT /api/v1/estatus-limpieza/{id_estatus_limpieza}`

**Objetivo**: Actualizar información de un estatus de limpieza.

**Autenticación**: Requerida

**Path Parameters**:
- `id_estatus_limpieza` (integer, requerido): ID del estatus

**Errores Posibles**:
- `404 Not Found`: Estatus no encontrado

---

#### Eliminar Estatus de Limpieza
**Endpoint**: `DELETE /api/v1/estatus-limpieza/{id_estatus_limpieza}`

**Objetivo**: Eliminar un estatus de limpieza (marcar como inactivo).

**Autenticación**: Requerida

**Path Parameters**:
- `id_estatus_limpieza` (integer, requerido): ID del estatus

**Response Exitosa (200 OK)**:
```json
{
  "mensaje": "Estatus marcado como inactivo correctamente"
}
```

**Nota**: Es una eliminación lógica, no física.

---

## 7. Mantenimiento

### 7.1. Listar Mantenimientos

**Endpoint**: `GET /api/v1/mantenimientos/`

**Objetivo**: Obtener lista de todos los mantenimientos.

**Autenticación**: Requerida

**Response Exitosa (200 OK)**: Lista de mantenimientos

---

### 7.2. Obtener Mantenimiento por ID

**Endpoint**: `GET /api/v1/mantenimientos/{id_mantenimiento}`

**Objetivo**: Obtener información de un mantenimiento específico.

**Autenticación**: Requerida

**Path Parameters**:
- `id_mantenimiento` (integer, requerido): ID del mantenimiento

**Errores Posibles**:
- `404 Not Found`: Mantenimiento no encontrado

---

### 7.3. Crear Mantenimiento

**Endpoint**: `POST /api/v1/mantenimientos/`

**Objetivo**: Crear un nuevo mantenimiento.

**Autenticación**: Requerida

**Request Body**:
```json
{
  "habitacion_area_id": 10,
  "empleado_id": 5,
  "fecha_inicio": "2024-12-01T08:00:00",
  "fecha_fin": "2024-12-01T12:00:00",
  "descripcion": "Mantenimiento preventivo",
  "estatus_id": 1
}
```

---

### 7.4. Actualizar Mantenimiento

**Endpoint**: `PUT /api/v1/mantenimientos/{id_mantenimiento}`

**Objetivo**: Actualizar información de un mantenimiento.

**Autenticación**: Requerida

**Path Parameters**:
- `id_mantenimiento` (integer, requerido): ID del mantenimiento

---

### 7.5. Eliminar Mantenimiento

**Endpoint**: `DELETE /api/v1/mantenimientos/{id_mantenimiento}`

**Objetivo**: Eliminar un mantenimiento.

**Autenticación**: Requerida

**Path Parameters**:
- `id_mantenimiento` (integer, requerido): ID del mantenimiento

---

### 7.6. Obtener Mantenimientos por Fecha

**Endpoint**: `GET /api/v1/mantenimientos/fecha/?fecha_inicio={fecha_inicio}`

**Objetivo**: Obtener mantenimientos de una fecha específica.

**Autenticación**: Requerida

**Query Parameters**:
- `fecha_inicio` (datetime, requerido): Fecha exacta de inicio del mantenimiento (YYYY-MM-DD)

**Ejemplo**:
```
GET /api/v1/mantenimientos/fecha/?fecha_inicio=2024-12-01T00:00:00
```

**Errores Posibles**:
- `404 Not Found`: No se encontraron mantenimientos para esa fecha

---

### 7.7. Obtener Mantenimientos por Habitación

**Endpoint**: `GET /api/v1/mantenimientos/habitacion-area/{habitacion_area_id}`

**Objetivo**: Obtener todos los mantenimientos de una habitación específica.

**Autenticación**: Requerida

**Path Parameters**:
- `habitacion_area_id` (integer, requerido): ID de la habitación

---

### 7.8. Obtener Mantenimientos por Empleado

**Endpoint**: `GET /api/v1/mantenimientos/empleado/{empleado_id}`

**Objetivo**: Obtener todos los mantenimientos asignados a un empleado.

**Autenticación**: Requerida

**Path Parameters**:
- `empleado_id` (integer, requerido): ID del empleado

---

### 7.9. Incidencias

#### Listar Incidencias
**Endpoint**: `GET /api/v1/incidencias/`

**Objetivo**: Obtener lista de todas las incidencias.

**Autenticación**: Requerida

**Response Exitosa (200 OK)**: Lista de incidencias

---

#### Obtener Incidencia por ID
**Endpoint**: `GET /api/v1/incidencias/{id_incidencia}`

**Objetivo**: Obtener información de una incidencia específica.

**Autenticación**: Requerida

**Path Parameters**:
- `id_incidencia` (integer, requerido): ID de la incidencia

**Errores Posibles**:
- `404 Not Found`: Incidencia no encontrada

---

#### Crear Incidencia
**Endpoint**: `POST /api/v1/incidencias/`

**Objetivo**: Crear una nueva incidencia.

**Autenticación**: Requerida

**Request Body**:
```json
{
  "habitacion_area_id": 10,
  "descripcion": "Fuga de agua en el baño",
  "estatus_id": 1,
  "fecha_reporte": "2024-12-01T10:00:00"
}
```

**Response Exitosa (200 OK)**: Objeto IncidenciaResponse

---

#### Actualizar Incidencia
**Endpoint**: `PUT /api/v1/incidencias/{id_incidencia}`

**Objetivo**: Actualizar información de una incidencia.

**Autenticación**: Requerida

**Path Parameters**:
- `id_incidencia` (integer, requerido): ID de la incidencia

**Errores Posibles**:
- `404 Not Found`: Incidencia no encontrada

---

#### Eliminar Incidencia
**Endpoint**: `DELETE /api/v1/incidencias/{id_incidencia}`

**Objetivo**: Eliminar una incidencia.

**Autenticación**: Requerida

**Path Parameters**:
- `id_incidencia` (integer, requerido): ID de la incidencia

**Response Exitosa (200 OK)**: Objeto IncidenciaResponse eliminado

---

#### Obtener Incidencias por Estatus
**Endpoint**: `GET /api/v1/incidencias/estatus/{id_estatus}`

**Objetivo**: Obtener todas las incidencias con un estatus específico.

**Autenticación**: Requerida

**Path Parameters**:
- `id_estatus` (integer, requerido): ID del estatus

**Response Exitosa (200 OK)**: Lista de incidencias con ese estatus

**Errores Posibles**:
- `404 Not Found`: No se encontraron incidencias con ese estatus

---

#### Obtener Incidencias por Habitación
**Endpoint**: `GET /api/v1/incidencias/habitacion/{habitacion_area_id}`

**Objetivo**: Obtener todas las incidencias de una habitación o área, ordenadas por estatus.

**Autenticación**: Requerida

**Path Parameters**:
- `habitacion_area_id` (integer, requerido): ID de la habitación o área

**Response Exitosa (200 OK)**: Lista de incidencias de la habitación

**Errores Posibles**:
- `404 Not Found`: No se encontraron incidencias para esa habitación o área

---

#### Obtener Incidencias por Fecha
**Endpoint**: `GET /api/v1/incidencias/fecha/{fecha_inicio}`

**Objetivo**: Obtener incidencias con fecha mayor o igual a la indicada, ordenadas por estatus.

**Autenticación**: Requerida

**Path Parameters**:
- `fecha_inicio` (datetime, requerido): Fecha de inicio (formato: YYYY-MM-DDTHH:MM:SS)

**Ejemplo**:
```
GET /api/v1/incidencias/fecha/2024-12-01T00:00:00
```

**Response Exitosa (200 OK)**: Lista de incidencias a partir de esa fecha

**Errores Posibles**:
- `404 Not Found`: No se encontraron incidencias a partir de esa fecha

---

#### Asociar Incidencia a Mantenimiento
**Endpoint**: `POST /api/v1/incidencias/{id_incidencia}/mantenimientos/{id_mantenimiento}`

**Objetivo**: Asociar una incidencia a un mantenimiento.

**Autenticación**: Requerida

**Path Parameters**:
- `id_incidencia` (integer, requerido): ID de la incidencia
- `id_mantenimiento` (integer, requerido): ID del mantenimiento

**Response Exitosa (200 OK)**: Confirmación de asociación

---

## 8. Catálogos

### 8.1. Países

#### Listar Países
**Endpoint**: `GET /api/v1/paises/`

**Query Parameters**:
- `skip` (integer, opcional): Número de registros a saltar (default: 0)
- `limit` (integer, opcional): Número máximo de registros (default: 100, máximo: 1000)

#### Obtener País por ID
**Endpoint**: `GET /api/v1/paises/{id_pais}`

#### Obtener País por Nombre
**Endpoint**: `GET /api/v1/paises/nombre/{nombre}`

#### Crear País
**Endpoint**: `POST /api/v1/paises/`

**Request Body**:
```json
{
  "nombre": "España",
  "id_estatus": 1
}
```

#### Actualizar País
**Endpoint**: `PUT /api/v1/paises/{id_pais}`

#### Eliminar País
**Endpoint**: `DELETE /api/v1/paises/{id_pais}`

#### Reactivar País
**Endpoint**: `PATCH /api/v1/paises/{id_pais}/reactivate`

---

### 8.2. Estados

#### Listar Estados
**Endpoint**: `GET /api/v1/estados/`

**Query Parameters**:
- `skip` (integer, opcional): Número de registros a saltar
- `limit` (integer, opcional): Número máximo de registros

#### Obtener Estados por País
**Endpoint**: `GET /api/v1/estados/pais/{id_pais}`

**Objetivo**: Obtener todos los estados de un país específico.

**Path Parameters**:
- `id_pais` (integer, requerido): ID del país

#### Obtener Estado por ID
**Endpoint**: `GET /api/v1/estados/{id_estado}`

#### Obtener Estado por Nombre
**Endpoint**: `GET /api/v1/estados/nombre/{nombre}`

#### Crear Estado
**Endpoint**: `POST /api/v1/estados/`

**Request Body**:
```json
{
  "id_pais": 1,
  "nombre": "Madrid",
  "id_estatus": 1
}
```

#### Actualizar Estado
**Endpoint**: `PUT /api/v1/estados/{id_estado}`

#### Eliminar Estado
**Endpoint**: `DELETE /api/v1/estados/{id_estado}`

#### Reactivar Estado
**Endpoint**: `PATCH /api/v1/estados/{id_estado}/reactivate`

---

### 8.3. Periodicidades

#### Listar Periodicidades
**Endpoint**: `GET /api/v1/periodicidades/`

**Objetivo**: Obtener lista de periodicidades disponibles (Diario, Semanal, Mensual, etc.).

**Autenticación**: Requerida

**Query Parameters**:
- `skip` (integer, opcional): Número de registros a saltar (default: 0)
- `limit` (integer, opcional): Número máximo de registros (default: 100)

**Response Exitosa (200 OK)**: Lista de periodicidades

---

#### Obtener Periodicidad por ID
**Endpoint**: `GET /api/v1/periodicidades/{id_periodicidad}`

**Objetivo**: Obtener información de una periodicidad específica.

**Autenticación**: Requerida

**Path Parameters**:
- `id_periodicidad` (integer, requerido): ID de la periodicidad

---

#### Crear Periodicidad
**Endpoint**: `POST /api/v1/periodicidades/`

**Objetivo**: Crear una nueva periodicidad.

**Autenticación**: Requerida

**Request Body**:
```json
{
  "periodicidad": "Diario",
  "descripcion": "Mantenimiento diario"
}
```

**Response Exitosa (201 Created)**: Objeto PeriodicidadResponse

---

#### Actualizar Periodicidad
**Endpoint**: `PUT /api/v1/periodicidades/{id_periodicidad}`

**Objetivo**: Actualizar información de una periodicidad.

**Autenticación**: Requerida

**Path Parameters**:
- `id_periodicidad` (integer, requerido): ID de la periodicidad

---

#### Eliminar Periodicidad
**Endpoint**: `DELETE /api/v1/periodicidades/{id_periodicidad}`

**Objetivo**: Eliminar una periodicidad.

**Autenticación**: Requerida

**Path Parameters**:
- `id_periodicidad` (integer, requerido): ID de la periodicidad

---

## 9. Email

### 9.1. Enviar Email

**Endpoint**: `POST /api/v1/emails/send`

**Objetivo**: Enviar un email básico (útil para testing del servicio SMTP).

**Autenticación**: No requerida (para testing)

**Request Body**:
```json
{
  "destinatario_email": "destinatario@email.com",
  "asunto": "Prueba de Email",
  "contenido_html": "<h1>Hola</h1><p>Este es un email de prueba.</p>"
}
```

**Parámetros**:
- `destinatario_email` (string, requerido): Email del destinatario
- `asunto` (string, requerido): Asunto del email
- `contenido_html` (string, requerido): Contenido HTML del email

**Response Exitosa (200 OK)**:
```json
{
  "success": true,
  "message": "Email enviado exitosamente",
  "email_id": 123
}
```

---

### 9.2. Consultar Logs de Emails

**Endpoint**: `GET /api/v1/emails/logs`

**Objetivo**: Consultar historial de emails enviados con filtros opcionales.

**Autenticación**: Requerida

**Query Parameters**:
- `skip` (integer, opcional): Número de registros a saltar
- `limit` (integer, opcional): Número máximo de registros
- `destinatario_email` (string, opcional): Filtrar por destinatario
- `estado` (string, opcional): Filtrar por estado (enviado, fallido, etc.)

**Response Exitosa (200 OK)**:
```json
[
  {
    "id_log": 1,
    "destinatario_email": "destinatario@email.com",
    "asunto": "Prueba de Email",
    "estado": "enviado",
    "fecha_envio": "2024-12-01T10:00:00",
    "error": null
  }
]
```

---

### 9.3. Obtener Log de Email por ID

**Endpoint**: `GET /api/v1/emails/logs/{id_log}`

**Objetivo**: Obtener información detallada de un log de email específico.

**Autenticación**: Requerida

**Path Parameters**:
- `id_log` (integer, requerido): ID del log

---

### 9.4. Listar Plantillas de Email

**Endpoint**: `GET /api/v1/emails/templates`

**Objetivo**: Obtener lista de plantillas de email disponibles.

**Autenticación**: Requerida

**Response Exitosa (200 OK)**:
```json
[
  {
    "id_template": 1,
    "nombre": "Bienvenida",
    "tipo": "welcome_user",
    "descripcion": "Plantilla de bienvenida para nuevos usuarios"
  }
]
```

---

### 9.5. Obtener Plantilla por ID

**Endpoint**: `GET /api/v1/emails/templates/{id_template}`

**Objetivo**: Obtener una plantilla de email específica.

**Autenticación**: Requerida

**Path Parameters**:
- `id_template` (integer, requerido): ID de la plantilla

---

## 10. Almacenamiento de Imágenes

### 10.1. Actualizar Foto de Perfil de Usuario

**Endpoint**: `PUT /api/v1/imagenes/foto/perfil/{id_usuario}`

**Objetivo**: Actualizar o subir la foto de perfil de un usuario.

**Autenticación**: Requerida

**Path Parameters**:
- `id_usuario` (integer, requerido): ID del usuario

**Request**: Form-data con archivo
- `file` (file, requerido): Archivo de imagen (JPG, PNG, GIF)

**Response Exitosa (200 OK)**:
```json
{
  "success": true,
  "message": "Foto de perfil actualizada exitosamente",
  "ruta_storage": "usuarios/perfil/1.jpg",
  "url_publica": "https://innpulse360.supabase.co/storage/v1/object/public/images/usuarios/perfil/1.jpg"
}
```

**Ejemplo cURL**:
```bash
curl -X PUT "http://localhost:8000/api/v1/imagenes/foto/perfil/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/image.jpg"
```

---

### 10.2. Imágenes de Hoteles

#### Actualizar Foto de Perfil de Hotel
**Endpoint**: `PUT /api/v1/hotel/{id_hotel}/foto-perfil`

**Objetivo**: Actualizar o subir la foto de perfil de un hotel.

**Autenticación**: Requerida

**Path Parameters**:
- `id_hotel` (integer, requerido): ID del hotel

**Request**: Form-data con archivo
- `file` (file, requerido): Archivo de imagen (JPG, PNG, WebP)

**Response Exitosa (200 OK)**:
```json
{
  "success": true,
  "path": "hotel/1/1.jpg",
  "bucket": "images",
  "public_url": "https://innpulse360.supabase.co/storage/v1/object/public/images/hotel/1/1.jpg",
  "message": "Foto de perfil actualizada exitosamente"
}
```

**Nota**: Si ya existe una foto de perfil, será reemplazada automáticamente.

---

#### Restaurar Foto de Perfil por Defecto de Hotel
**Endpoint**: `DELETE /api/v1/hotel/{id_hotel}/foto-perfil`

**Objetivo**: Restaurar la foto de perfil de un hotel a la imagen por defecto.

**Autenticación**: Requerida

**Path Parameters**:
- `id_hotel` (integer, requerido): ID del hotel

**Response Exitosa (200 OK)**:
```json
{
  "success": true,
  "message": "Foto de perfil restaurada al valor por defecto"
}
```

---

#### Subir Imagen a Galería de Hotel
**Endpoint**: `POST /api/v1/hotel/{id_hotel}/galeria`

**Objetivo**: Subir una imagen a la galería del hotel.

**Autenticación**: Requerida

**Path Parameters**:
- `id_hotel` (integer, requerido): ID del hotel

**Request**: Form-data con archivo
- `file` (file, requerido): Archivo de imagen (JPG, PNG, WebP)

**Response Exitosa (201 Created)**:
```json
{
  "success": true,
  "path": "hotel/1/galeria/img_1_itema1b2c3d4.jpg",
  "bucket": "images",
  "public_url": "https://innpulse360.supabase.co/storage/v1/object/public/images/hotel/1/galeria/img_1_itema1b2c3d4.jpg",
  "message": "Imagen agregada a la galería exitosamente"
}
```

**Nota**: El nombre del archivo se genera automáticamente.

---

#### Listar Imágenes de Galería de Hotel
**Endpoint**: `GET /api/v1/hotel/{id_hotel}/galeria`

**Objetivo**: Listar todas las imágenes de la galería de un hotel.

**Autenticación**: Requerida

**Path Parameters**:
- `id_hotel` (integer, requerido): ID del hotel

**Response Exitosa (200 OK)**:
```json
{
  "success": true,
  "imagenes": [
    {
      "nombre": "img_1_itema1b2c3d4.jpg",
      "url_publica": "https://innpulse360.supabase.co/storage/v1/object/public/images/hotel/1/galeria/img_1_itema1b2c3d4.jpg",
      "tamaño": 123456
    }
  ],
  "total": 5,
  "message": null
}
```

---

#### Eliminar Imagen de Galería de Hotel
**Endpoint**: `DELETE /api/v1/hotel/{id_hotel}/galeria/{nombre_archivo}`

**Objetivo**: Eliminar una imagen específica de la galería del hotel.

**Autenticación**: Requerida

**Path Parameters**:
- `id_hotel` (integer, requerido): ID del hotel
- `nombre_archivo` (string, requerido): Nombre del archivo a eliminar (ej: "1a2b3c.jpg")

**Response Exitosa (200 OK)**:
```json
{
  "success": true,
  "message": "Imagen '1a2b3c.jpg' eliminada exitosamente de la galería"
}
```

---

### 10.3. Imágenes de Habitaciones

#### Subir Imagen a Galería de Habitación
**Endpoint**: `POST /api/v1/habitaciones/{id_habitacion_area}/galeria`

**Objetivo**: Subir una imagen a la galería de una habitación.

**Autenticación**: Requerida

**Path Parameters**:
- `id_habitacion_area` (integer, requerido): ID de la habitación

**Request**: Form-data con archivo
- `file` (file, requerido): Archivo de imagen (JPG, PNG, WebP)

**Response Exitosa (201 Created)**: Objeto HotelFotoPerfilResponse con URL pública

---

#### Listar Imágenes de Galería de Habitación
**Endpoint**: `GET /api/v1/habitaciones/{id_habitacion_area}/galeria`

**Objetivo**: Listar todas las imágenes de la galería de una habitación.

**Autenticación**: Requerida

**Path Parameters**:
- `id_habitacion_area` (integer, requerido): ID de la habitación

**Response Exitosa (200 OK)**: Objeto GaleriaListResponse con lista de imágenes

---

#### Eliminar Imagen de Galería de Habitación
**Endpoint**: `DELETE /api/v1/habitaciones/{id_habitacion_area}/galeria/{nombre_archivo}`

**Objetivo**: Eliminar una imagen específica de la galería de la habitación.

**Autenticación**: Requerida

**Path Parameters**:
- `id_habitacion_area` (integer, requerido): ID de la habitación
- `nombre_archivo` (string, requerido): Nombre del archivo a eliminar

---

### 10.4. Imágenes de Limpieza

#### Subir Imagen a Galería de Limpieza
**Endpoint**: `POST /api/v1/limpiezas/{id_limpieza}/galeria?tipo={tipo}`

**Objetivo**: Subir una imagen a la galería de una limpieza (antes o después).

**Autenticación**: Requerida

**Path Parameters**:
- `id_limpieza` (integer, requerido): ID de la limpieza

**Query Parameters**:
- `tipo` (string, requerido): Tipo de imagen - "antes" o "despues"

**Request**: Form-data con archivo
- `file` (file, requerido): Archivo de imagen (JPG, PNG, WebP)

**Response Exitosa (201 Created)**: Objeto HotelFotoPerfilResponse

**Ejemplo**:
```
POST /api/v1/limpiezas/5/galeria?tipo=antes
```

---

#### Listar Imágenes de Galería de Limpieza
**Endpoint**: `GET /api/v1/limpiezas/{id_limpieza}/galeria?tipo={tipo}`

**Objetivo**: Listar imágenes de la galería de una limpieza.

**Autenticación**: Requerida

**Path Parameters**:
- `id_limpieza` (integer, requerido): ID de la limpieza

**Query Parameters**:
- `tipo` (string, opcional): Tipo de imagen a listar - "antes", "despues" o None para ambas

**Response Exitosa (200 OK)**: Objeto GaleriaListResponse

**Nota**: Si no se especifica `tipo`, retorna todas las imágenes (antes y después) con el campo `tipo` indicando su categoría.

---

#### Eliminar Imagen de Galería de Limpieza
**Endpoint**: `DELETE /api/v1/limpiezas/{id_limpieza}/galeria/{nombre_archivo}?tipo={tipo}`

**Objetivo**: Eliminar una imagen específica de la galería de la limpieza.

**Autenticación**: Requerida

**Path Parameters**:
- `id_limpieza` (integer, requerido): ID de la limpieza
- `nombre_archivo` (string, requerido): Nombre del archivo a eliminar

**Query Parameters**:
- `tipo` (string, requerido): Tipo de imagen - "antes" o "despues"

---

### 10.5. Imágenes de Mantenimiento

#### Subir Imagen a Galería de Mantenimiento
**Endpoint**: `POST /api/v1/mantenimientos/{id_mantenimiento}/galeria?tipo={tipo}`

**Objetivo**: Subir una imagen a la galería de un mantenimiento (antes o después).

**Autenticación**: Requerida

**Path Parameters**:
- `id_mantenimiento` (integer, requerido): ID del mantenimiento

**Query Parameters**:
- `tipo` (string, requerido): Tipo de imagen - "antes" o "despues"

**Request**: Form-data con archivo
- `file` (file, requerido): Archivo de imagen (JPG, PNG, WebP)

**Response Exitosa (201 Created)**: Objeto HotelFotoPerfilResponse

---

#### Listar Imágenes de Galería de Mantenimiento
**Endpoint**: `GET /api/v1/mantenimientos/{id_mantenimiento}/galeria?tipo={tipo}`

**Objetivo**: Listar imágenes de la galería de un mantenimiento.

**Autenticación**: Requerida

**Path Parameters**:
- `id_mantenimiento` (integer, requerido): ID del mantenimiento

**Query Parameters**:
- `tipo` (string, opcional): Tipo de imagen a listar - "antes", "despues" o None para ambas

**Response Exitosa (200 OK)**: Objeto GaleriaListResponse

---

#### Eliminar Imagen de Galería de Mantenimiento
**Endpoint**: `DELETE /api/v1/mantenimientos/{id_mantenimiento}/galeria/{nombre_archivo}?tipo={tipo}`

**Objetivo**: Eliminar una imagen específica de la galería del mantenimiento.

**Autenticación**: Requerida

**Path Parameters**:
- `id_mantenimiento` (integer, requerido): ID del mantenimiento
- `nombre_archivo` (string, requerido): Nombre del archivo a eliminar

**Query Parameters**:
- `tipo` (string, requerido): Tipo de imagen - "antes" o "despues"

---

### 10.6. Imágenes de Tipo de Habitación

#### Actualizar Foto de Perfil de Tipo de Habitación
**Endpoint**: `PUT /api/v1/tipo-habitacion/{id_tipoHabitacion}/foto-perfil`

**Objetivo**: Actualizar o subir la foto de perfil de un tipo de habitación.

**Autenticación**: Requerida

**Path Parameters**:
- `id_tipoHabitacion` (integer, requerido): ID del tipo de habitación

**Request**: Form-data con archivo
- `file` (file, requerido): Archivo de imagen (JPG, PNG, WebP)

**Response Exitosa (200 OK)**: Objeto HotelFotoPerfilResponse

---

#### Restaurar Foto de Perfil por Defecto de Tipo de Habitación
**Endpoint**: `DELETE /api/v1/tipo-habitacion/{id_tipoHabitacion}/foto-perfil`

**Objetivo**: Restaurar la foto de perfil de un tipo de habitación a la imagen por defecto.

**Autenticación**: Requerida

**Path Parameters**:
- `id_tipoHabitacion` (integer, requerido): ID del tipo de habitación

---

#### Subir Imagen a Galería de Tipo de Habitación
**Endpoint**: `POST /api/v1/tipo-habitacion/{id_tipoHabitacion}/galeria`

**Objetivo**: Subir una imagen a la galería del tipo de habitación.

**Autenticación**: Requerida

**Path Parameters**:
- `id_tipoHabitacion` (integer, requerido): ID del tipo de habitación

**Request**: Form-data con archivo
- `file` (file, requerido): Archivo de imagen (JPG, PNG, WebP)

**Response Exitosa (201 Created)**: Objeto HotelFotoPerfilResponse

---

#### Listar Imágenes de Galería de Tipo de Habitación
**Endpoint**: `GET /api/v1/tipo-habitacion/{id_tipoHabitacion}/galeria`

**Objetivo**: Listar todas las imágenes de la galería de un tipo de habitación.

**Autenticación**: Requerida

**Path Parameters**:
- `id_tipoHabitacion` (integer, requerido): ID del tipo de habitación

**Response Exitosa (200 OK)**: Objeto GaleriaListResponse

---

#### Eliminar Imagen de Galería de Tipo de Habitación
**Endpoint**: `DELETE /api/v1/tipo-habitacion/{id_tipoHabitacion}/galeria/{nombre_archivo}`

**Objetivo**: Eliminar una imagen específica de la galería del tipo de habitación.

**Autenticación**: Requerida

**Path Parameters**:
- `id_tipoHabitacion` (integer, requerido): ID del tipo de habitación
- `nombre_archivo` (string, requerido): Nombre del archivo a eliminar

---

### 10.7. Imágenes de Incidencias

#### Subir Imagen a Galería de Incidencia
**Endpoint**: `POST /api/v1/incidencias/{id_incidencia}/galeria`

**Objetivo**: Subir una imagen a la galería de una incidencia.

**Autenticación**: Requerida

**Path Parameters**:
- `id_incidencia` (integer, requerido): ID de la incidencia

**Request**: Form-data con archivo
- `file` (file, requerido): Archivo de imagen (JPG, PNG, WebP)

**Response Exitosa (201 Created)**: Objeto HotelFotoPerfilResponse

**Nota**: El nombre del archivo se genera automáticamente.

---

#### Listar Imágenes de Galería de Incidencia
**Endpoint**: `GET /api/v1/incidencias/{id_incidencia}/galeria`

**Objetivo**: Listar todas las imágenes de la galería de una incidencia.

**Autenticación**: Requerida

**Path Parameters**:
- `id_incidencia` (integer, requerido): ID de la incidencia

**Response Exitosa (200 OK)**: Objeto GaleriaListResponse

---

#### Eliminar Imagen de Galería de Incidencia
**Endpoint**: `DELETE /api/v1/incidencias/{id_incidencia}/galeria/{nombre_archivo}`

**Objetivo**: Eliminar una imagen específica de la galería de la incidencia.

**Autenticación**: Requerida

**Path Parameters**:
- `id_incidencia` (integer, requerido): ID de la incidencia
- `nombre_archivo` (string, requerido): Nombre del archivo a eliminar

**Response Exitosa (200 OK)**:
```json
{
  "success": true,
  "message": "Imagen 'nombre_archivo.jpg' eliminada exitosamente de la galería"
}
```

---

## 11. Seguridad y Roles

### 11.1. Roles

#### Crear Rol
**Endpoint**: `POST /api/v1/roles/`

**Objetivo**: Crear un nuevo rol en el sistema.

**Autenticación**: Requerida

**Request Body**:
```json
{
  "rol": "Administrador",
  "descripcion": "Rol con permisos completos",
  "estatus_id": 1
}
```

**Parámetros**:
- `rol` (string, requerido): Nombre del rol (único)
- `descripcion` (string, opcional): Descripción del rol
- `estatus_id` (integer, opcional): Estatus del rol (1=Activo por defecto)

**Response Exitosa (201 Created)**: Objeto RolesResponse

---

#### Listar Roles
**Endpoint**: `GET /api/v1/roles/`

**Objetivo**: Obtener lista de roles activos con paginación.

**Autenticación**: Requerida

**Query Parameters**:
- `skip` (integer, opcional): Número de registros a saltar (default: 0)
- `limit` (integer, opcional): Número máximo de registros (default: 100, máximo: 1000)

**Response Exitosa (200 OK)**: Lista de roles

---

#### Obtener Rol por ID
**Endpoint**: `GET /api/v1/roles/{id_rol}`

**Objetivo**: Obtener información de un rol específico.

**Autenticación**: Requerida

**Path Parameters**:
- `id_rol` (integer, requerido): ID del rol

**Errores Posibles**:
- `404 Not Found`: Rol no encontrado

---

#### Obtener Rol por Nombre
**Endpoint**: `GET /api/v1/roles/by-name/{rol}`

**Objetivo**: Obtener un rol por su nombre.

**Autenticación**: Requerida

**Path Parameters**:
- `rol` (string, requerido): Nombre del rol

**Errores Posibles**:
- `404 Not Found`: Rol no encontrado

---

#### Actualizar Rol
**Endpoint**: `PUT /api/v1/roles/{id_rol}`

**Objetivo**: Actualizar información de un rol.

**Autenticación**: Requerida

**Path Parameters**:
- `id_rol` (integer, requerido): ID del rol

**Request Body** (todos los campos son opcionales):
```json
{
  "rol": "Administrador Actualizado",
  "descripcion": "Nueva descripción"
}
```

---

#### Eliminar Rol
**Endpoint**: `DELETE /api/v1/roles/{id_rol}`

**Objetivo**: Eliminar un rol (eliminación lógica - cambia estatus a inactivo).

**Autenticación**: Requerida

**Path Parameters**:
- `id_rol` (integer, requerido): ID del rol

**Response Exitosa (204 No Content)**: Sin contenido

**Nota**: Eliminación lógica (cambia estatus a inactivo)

---

#### Reactivar Rol
**Endpoint**: `PATCH /api/v1/roles/{id_rol}/reactivate`

**Objetivo**: Reactivar un rol (cambiar estatus a activo).

**Autenticación**: Requerida

**Path Parameters**:
- `id_rol` (integer, requerido): ID del rol

**Response Exitosa (200 OK)**: Objeto RolesResponse reactivado

---

### 11.2. Usuario-Rol

#### Asignar Rol a Usuario
**Endpoint**: `POST /api/v1/usuarios/{usuario_id}/roles/{rol_id}`

**Objetivo**: Asignar un rol específico a un usuario.

**Autenticación**: Requerida

**Path Parameters**:
- `usuario_id` (integer, requerido): ID del usuario
- `rol_id` (integer, requerido): ID del rol a asignar

**Response Exitosa (201 Created)**:
```json
{
  "message": "Rol asignado exitosamente al usuario"
}
```

---

#### Remover Rol de Usuario
**Endpoint**: `DELETE /api/v1/usuarios/{usuario_id}/roles/{rol_id}`

**Objetivo**: Remover un rol específico de un usuario.

**Autenticación**: Requerida

**Path Parameters**:
- `usuario_id` (integer, requerido): ID del usuario
- `rol_id` (integer, requerido): ID del rol a remover

**Response Exitosa (204 No Content)**: Sin contenido

---

#### Obtener Roles de un Usuario
**Endpoint**: `GET /api/v1/usuarios/{usuario_id}/roles`

**Objetivo**: Obtener todos los roles asignados a un usuario.

**Autenticación**: Requerida

**Path Parameters**:
- `usuario_id` (integer, requerido): ID del usuario

**Response Exitosa (200 OK)**: Lista de roles del usuario

---

#### Asignar Múltiples Roles a Usuario
**Endpoint**: `PUT /api/v1/usuarios/{usuario_id}/roles`

**Objetivo**: Asignar múltiples roles a un usuario (solo los que no estén ya asignados).

**Autenticación**: Requerida

**Path Parameters**:
- `usuario_id` (integer, requerido): ID del usuario

**Request Body**:
```json
{
  "roles_ids": [1, 2, 3]
}
```

**Response Exitosa (200 OK)**:
```json
{
  "message": "Se asignaron 3 roles al usuario",
  "total_requested": 3,
  "assigned": 3,
  "skipped": 0
}
```

---

#### Remover Múltiples Roles de Usuario
**Endpoint**: `DELETE /api/v1/usuarios/{usuario_id}/roles`

**Objetivo**: Remover múltiples roles de un usuario.

**Autenticación**: Requerida

**Path Parameters**:
- `usuario_id` (integer, requerido): ID del usuario

**Request Body**:
```json
{
  "roles_ids": [1, 2]
}
```

**Response Exitosa (200 OK)**:
```json
{
  "message": "Se removieron 2 roles del usuario",
  "total_requested": 2,
  "removed": 2,
  "not_found": 0
}
```

---

#### Obtener Usuario con Roles
**Endpoint**: `GET /api/v1/usuarios/{usuario_id}/with-roles`

**Objetivo**: Obtener un usuario con todos sus roles incluidos.

**Autenticación**: Requerida

**Path Parameters**:
- `usuario_id` (integer, requerido): ID del usuario

**Response Exitosa (200 OK)**: Objeto UsuarioResponse con roles incluidos

---

#### Obtener Usuarios por Rol
**Endpoint**: `GET /api/v1/usuarios/by-rol/{rol_id}`

**Objetivo**: Obtener todos los usuarios que tienen un rol específico.

**Autenticación**: Requerida

**Path Parameters**:
- `rol_id` (integer, requerido): ID del rol

**Response Exitosa (200 OK)**: Lista de usuarios con ese rol

---

### 11.3. Módulos

#### Crear Módulo
**Endpoint**: `POST /api/v1/modulos/`

**Objetivo**: Crear un nuevo módulo del sistema.

**Autenticación**: Requerida

**Request Body**:
```json
{
  "nombre": "Dashboard",
  "descripcion": "Panel principal del sistema",
  "icono": "fas fa-dashboard",
  "ruta": "/dashboard",
  "id_estatus": 1
}
```

**Parámetros**:
- `nombre` (string, requerido): Nombre del módulo (máximo 25 caracteres)
- `descripcion` (string, opcional): Descripción del módulo (máximo 100 caracteres)
- `icono` (string, opcional): Icono del módulo (máximo 25 caracteres)
- `ruta` (string, opcional): Ruta del módulo (máximo 250 caracteres)
- `id_estatus` (integer, opcional): Estatus (1=Activo, 0=Inactivo)

**Response Exitosa (201 Created)**: Objeto ModulosResponse

---

#### Listar Módulos
**Endpoint**: `GET /api/v1/modulos/`

**Objetivo**: Obtener todos los módulos con paginación.

**Autenticación**: Requerida

**Query Parameters**:
- `skip` (integer, opcional): Número de registros a omitir (default: 0)
- `limit` (integer, opcional): Número máximo de registros (default: 100, máximo: 1000)
- `activos_only` (boolean, opcional): Solo obtener módulos activos (default: false)

**Response Exitosa (200 OK)**: Lista de módulos

---

#### Obtener Módulo por ID
**Endpoint**: `GET /api/v1/modulos/{id_modulo}`

**Objetivo**: Obtener información de un módulo específico.

**Autenticación**: Requerida

**Path Parameters**:
- `id_modulo` (integer, requerido): ID del módulo

**Response Exitosa (200 OK)**: Objeto ModulosResponse

---

#### Actualizar Módulo
**Endpoint**: `PUT /api/v1/modulos/{id_modulo}`

**Objetivo**: Actualizar información de un módulo.

**Autenticación**: Requerida

**Path Parameters**:
- `id_modulo` (integer, requerido): ID del módulo

**Request Body** (todos los campos son opcionales):
```json
{
  "nombre": "Dashboard Actualizado",
  "descripcion": "Nueva descripción"
}
```

---

#### Eliminar Módulo
**Endpoint**: `DELETE /api/v1/modulos/{id_modulo}`

**Objetivo**: Eliminar un módulo (soft delete).

**Autenticación**: Requerida

**Path Parameters**:
- `id_modulo` (integer, requerido): ID del módulo

**Response Exitosa (204 No Content)**: Sin contenido

---

#### Buscar Módulo por Nombre
**Endpoint**: `GET /api/v1/modulos/buscar/nombre/{nombre}`

**Objetivo**: Buscar un módulo por su nombre.

**Autenticación**: Requerida

**Path Parameters**:
- `nombre` (string, requerido): Nombre del módulo a buscar

**Response Exitosa (200 OK)**: Objeto ModulosResponse o null si no se encuentra

---

#### Obtener Módulos Activos
**Endpoint**: `GET /api/v1/modulos/activos/`

**Objetivo**: Obtener solo los módulos activos.

**Autenticación**: Requerida

**Query Parameters**:
- `skip` (integer, opcional): Número de registros a omitir
- `limit` (integer, opcional): Número máximo de registros

---

#### Asignar Módulo a Rol
**Endpoint**: `POST /api/v1/modulos/asignar-rol`

**Objetivo**: Asignar un módulo a un rol.

**Autenticación**: Requerida

**Request Body**:
```json
{
  "modulo_id": 1,
  "rol_id": 2
}
```

**Response Exitosa (200 OK)**:
```json
{
  "message": "Módulo asignado al rol correctamente"
}
```

---

#### Desasignar Módulo de Rol
**Endpoint**: `DELETE /api/v1/modulos/desasignar-rol?modulo_id={modulo_id}&rol_id={rol_id}`

**Objetivo**: Desasignar un módulo de un rol.

**Autenticación**: Requerida

**Query Parameters**:
- `modulo_id` (integer, requerido): ID del módulo
- `rol_id` (integer, requerido): ID del rol

**Response Exitosa (200 OK)**:
```json
{
  "message": "Módulo desasignado del rol correctamente"
}
```

---

#### Asignar Múltiples Módulos a Rol
**Endpoint**: `POST /api/v1/modulos/asignar-multiples`

**Objetivo**: Asignar múltiples módulos a un rol.

**Autenticación**: Requerida

**Request Body**:
```json
{
  "rol_id": 2,
  "modulos_ids": [1, 2, 3, 5]
}
```

**Response Exitosa (200 OK)**:
```json
{
  "message": "Módulos asignados al rol correctamente"
}
```

---

#### Obtener Módulos por Rol
**Endpoint**: `GET /api/v1/modulos/por-rol/{rol_id}`

**Objetivo**: Obtener todos los módulos asignados a un rol.

**Autenticación**: Requerida

**Path Parameters**:
- `rol_id` (integer, requerido): ID del rol

**Response Exitosa (200 OK)**: Lista de módulos del rol

---

## Errores Comunes y Soluciones

### Error 401 Unauthorized

**Causa**: Token inválido, expirado o ausente.

**Solución**:
1. Verificar que el token esté incluido en el header `Authorization`
2. Verificar que el token no haya expirado (duración: 30 minutos)
3. Volver a autenticarse para obtener un nuevo token

**Ejemplo de error**:
```json
{
  "detail": "Token inválido o expirado"
}
```

---

### Error 400 Bad Request

**Causa**: Datos inválidos en la petición.

**Solución**:
1. Verificar que todos los campos requeridos estén presentes
2. Verificar que los tipos de datos sean correctos
3. Verificar validaciones específicas (RFC único, email único, etc.)

**Ejemplo de error**:
```json
{
  "detail": "El RFC 'PEGJ800101XXX' ya está registrado"
}
```

---

### Error 404 Not Found

**Causa**: Recurso no encontrado.

**Solución**:
1. Verificar que el ID del recurso sea correcto
2. Verificar que el recurso no haya sido eliminado

**Ejemplo de error**:
```json
{
  "detail": "Hotel con ID 999 no encontrado"
}
```

---

### Error 500 Internal Server Error

**Causa**: Error interno del servidor.

**Solución**:
1. Verificar los logs del servidor
2. Contactar al administrador del sistema
3. Verificar que la base de datos esté disponible

---

## Ejemplos de Integración

### JavaScript (Fetch API)

```javascript
// Obtener token
async function login(login, password) {
  const response = await fetch('http://localhost:8000/api/v1/usuarios/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ login, password })
  });
  
  const data = await response.json();
  return data.access_token;
}

// Usar token para obtener hoteles
async function getHoteles(token) {
  const response = await fetch('http://localhost:8000/api/v1/hotel/', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  
  return await response.json();
}

// Uso
const token = await login('juan.perez', 'Password123');
const hoteles = await getHoteles(token);
console.log(hoteles);
```

---

### Python (Requests)

```python
import requests

# Obtener token
def login(login, password):
    url = 'http://localhost:8000/api/v1/usuarios/login'
    response = requests.post(url, json={
        'login': login,
        'password': password
    })
    return response.json()['access_token']

# Usar token para obtener hoteles
def get_hoteles(token):
    url = 'http://localhost:8000/api/v1/hotel/'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Uso
token = login('juan.perez', 'Password123')
hoteles = get_hoteles(token)
print(hoteles)
```

---

### cURL

```bash
# 1. Obtener token
TOKEN=$(curl -X POST "http://localhost:8000/api/v1/usuarios/login" \
  -H "Content-Type: application/json" \
  -d '{"login":"juan.perez","password":"Password123"}' \
  | jq -r '.access_token')

# 2. Usar token para obtener hoteles
curl -X GET "http://localhost:8000/api/v1/hotel/" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Notas Importantes

1. **Tokens JWT**: Los tokens expiran después de 30 minutos. Debes renovarlos periódicamente.

2. **Paginación**: Muchos endpoints de listado soportan paginación mediante `skip` y `limit`.

3. **Actualizaciones Parciales**: Los endpoints PUT aceptan actualizaciones parciales (solo envía los campos que deseas actualizar).

4. **Eliminación Lógica**: Muchos endpoints DELETE realizan eliminación lógica (cambian estatus a inactivo) en lugar de eliminación física.

5. **Validaciones**: El sistema valida automáticamente:
   - RFC único para clientes
   - Email único para usuarios
   - Login único para usuarios
   - Formatos de datos (fechas, emails, etc.)

6. **Almacenamiento de Imágenes**: Las imágenes se almacenan en Supabase Storage y se generan URLs públicas automáticamente.

7. **Documentación Interactiva**: Puedes probar todos los endpoints directamente en:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

---

**Última actualización**: Diciembre 2024  
**Versión de API**: 1.0.0


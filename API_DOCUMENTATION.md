# 📚 Documentación API - InnPulse360

**Base URL:** `http://localhost:8000`  
**API Version:** `/api/v1`  
**URL Completa Base:** `http://localhost:8000/api/v1`

---

## 📑 Tabla de Contenidos

1. [Autenticación y Usuarios](#1-autenticación-y-usuarios)
2. [Roles y Permisos](#2-roles-y-permisos)
3. [Módulos](#3-módulos)
4. [Clientes](#4-clientes)
5. [Hoteles](#5-hoteles)
6. [Tipos de Habitación](#6-tipos-de-habitación)
7. [Características](#7-características)
8. [Empleados](#8-empleados)
9. [Puestos](#9-puestos)
10. [Catálogos](#10-catálogos)
11. [Email](#11-email)

---

## 1. Autenticación y Usuarios

### 🔐 Login
**POST** `http://localhost:8000/api/v1/usuarios/login`

**Body:**
```json
{
  "login": "admin",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user_info": {
    "id_usuario": 1,
    "login": "admin",
    "correo_electronico": "admin@innpulse.com"
  }
}
```

---

### 👤 Crear Usuario
**POST** `http://localhost:8000/api/v1/usuarios/`

**Headers:**
```
Authorization: Bearer {token}
```

**Body:**
```json
{
  "login": "usuario123",
  "correo_electronico": "usuario@email.com",
  "password": "Password123",
  "estatus_id": 1,
  "roles_ids": [1, 2]
}
```

**Response:**
```json
{
  "id_usuario": 10,
  "login": "usuario123",
  "correo_electronico": "usuario@email.com",
  "estatus_id": 1,
  "roles": [
    {"id_rol": 1, "rol": "Administrador"},
    {"id_rol": 2, "rol": "Gerente"}
  ]
}
```

---

### 📋 Listar Usuarios
**GET** `http://localhost:8000/api/v1/usuarios/?skip=0&limit=100`

**Headers:**
```
Authorization: Bearer {token}
```

**Response:**
```json
[
  {
    "id_usuario": 1,
    "login": "admin",
    "correo_electronico": "admin@innpulse.com",
    "estatus_id": 1,
    "roles": [...]
  }
]
```

---

### 🔍 Obtener Usuario por ID
**GET** `http://localhost:8000/api/v1/usuarios/{id_usuario}`

**Headers:**
```
Authorization: Bearer {token}
```

**Ejemplo:** `http://localhost:8000/api/v1/usuarios/1`

---

### 🔍 Obtener Usuario por Login
**GET** `http://localhost:8000/api/v1/usuarios/login/{login}`

**Headers:**
```
Authorization: Bearer {token}
```

**Ejemplo:** `http://localhost:8000/api/v1/usuarios/login/admin`

---

### ✏️ Actualizar Usuario
**PUT** `http://localhost:8000/api/v1/usuarios/{id_usuario}`

**Headers:**
```
Authorization: Bearer {token}
```

**Body:** (todos los campos opcionales)
```json
{
  "login": "nuevo_login",
  "correo_electronico": "nuevo@email.com",
  "password": "NuevaPassword123",
  "estatus_id": 1
}
```

---

### 🗑️ Eliminar Usuario
**DELETE** `http://localhost:8000/api/v1/usuarios/{id_usuario}`

**Headers:**
```
Authorization: Bearer {token}
```

**Ejemplo:** `http://localhost:8000/api/v1/usuarios/10`

---

### 👨‍💼 Obtener Perfil Actual
**GET** `http://localhost:8000/api/v1/usuarios/me/profile`

**Headers:**
```
Authorization: Bearer {token}
```

---

### ✏️ Actualizar Perfil Actual
**PUT** `http://localhost:8000/api/v1/usuarios/me/profile`

**Headers:**
```
Authorization: Bearer {token}
```

**Body:**
```json
{
  "correo_electronico": "nuevo@email.com",
  "password": "NuevaPassword123"
}
```

---

### 🔍 Verificar Disponibilidad (Registro Cliente)
**POST** `http://localhost:8000/api/v1/usuarios/verificar-disponibilidad`

**Body:**
```json
{
  "login": "cliente123",
  "correo_electronico": "cliente@email.com"
}
```

**Response:**
```json
{
  "login_disponible": true,
  "correo_en_clientes": true,
  "cliente_encontrado": {
    "id_cliente": 123,
    "nombre_razon_social": "Juan Pérez González",
    "rfc": "PEGJ800101XXX",
    "tipo_persona": 1,
    "correo_electronico": "cliente@email.com"
  },
  "puede_registrar": true,
  "mensaje": "Login disponible. Se encontró cliente 'Juan Pérez González'"
}
```

---

### 📝 Registro Usuario-Cliente
**POST** `http://localhost:8000/api/v1/usuarios/registro-cliente`

**Body:**
```json
{
  "login": "cliente123",
  "correo_electronico": "cliente@email.com",
  "password": null,
  "cliente_id": 123
}
```

**Response:**
```json
{
  "usuario_creado": true,
  "id_usuario": 45,
  "login": "cliente123",
  "correo_electronico": "cliente@email.com",
  "cliente_asociado": {
    "id_cliente": 123,
    "nombre_razon_social": "Juan Pérez González",
    "rfc": "PEGJ800101XXX",
    "tipo_persona": 1,
    "correo_electronico": "cliente@email.com"
  },
  "rol_asignado": "Cliente",
  "password_temporal_generada": true,
  "password_temporal": "A1b2C3d4E5f6",
  "password_expira": "2024-01-22T10:30:00",
  "email_enviado": false,
  "mensaje": "Usuario creado y asociado al cliente exitosamente"
}
```

---

### 🔑 Cambiar Password Temporal
**POST** `http://localhost:8000/api/v1/usuarios/cambiar-password-temporal`

**Body:**
```json
{
  "login": "cliente123",
  "password_actual": "A1b2C3d4E5f6",
  "password_nueva": "MiNuevaPassword123",
  "password_confirmacion": "MiNuevaPassword123"
}
```

**Response:**
```json
{
  "success": true,
  "mensaje": "Contraseña actualizada exitosamente",
  "requiere_login": true
}
```

---

## 2. Roles y Permisos

### 📋 Listar Roles
**GET** `http://localhost:8000/api/v1/roles/?skip=0&limit=100`

**Headers:**
```
Authorization: Bearer {token}
```

**Response:**
```json
[
  {
    "id_rol": 1,
    "rol": "Administrador",
    "descripcion": "Rol de administrador del sistema",
    "estatus_id": 1,
    "usuarios": []
  }
]
```

---

### 👤 Crear Rol
**POST** `http://localhost:8000/api/v1/roles/`

**Headers:**
```
Authorization: Bearer {token}
```

**Body:**
```json
{
  "rol": "Gerente",
  "descripcion": "Gerente de hotel",
  "estatus_id": 1
}
```

---

### 🔍 Obtener Rol por ID
**GET** `http://localhost:8000/api/v1/roles/{id_rol}`

**Headers:**
```
Authorization: Bearer {token}
```

**Ejemplo:** `http://localhost:8000/api/v1/roles/1`

---

### ✏️ Actualizar Rol
**PUT** `http://localhost:8000/api/v1/roles/{id_rol}`

**Headers:**
```
Authorization: Bearer {token}
```

**Body:**
```json
{
  "rol": "Gerente Actualizado",
  "descripcion": "Descripción actualizada",
  "estatus_id": 1
}
```

---

### 🗑️ Eliminar Rol
**DELETE** `http://localhost:8000/api/v1/roles/{id_rol}`

**Headers:**
```
Authorization: Bearer {token}
```

---

### 🔗 Asignar Rol a Usuario
**POST** `http://localhost:8000/api/v1/usuario-rol/asignar`

**Headers:**
```
Authorization: Bearer {token}
```

**Body:**
```json
{
  "usuario_id": 10,
  "rol_id": 2
}
```

---

### 🔓 Desasignar Rol de Usuario
**DELETE** `http://localhost:8000/api/v1/usuario-rol/desasignar?usuario_id=10&rol_id=2`

**Headers:**
```
Authorization: Bearer {token}
```

---

### 📋 Obtener Roles de Usuario
**GET** `http://localhost:8000/api/v1/usuario-rol/usuario/{usuario_id}/roles`

**Headers:**
```
Authorization: Bearer {token}
```

**Ejemplo:** `http://localhost:8000/api/v1/usuario-rol/usuario/10/roles`

---

## 3. Módulos

### 📋 Listar Módulos
**GET** `http://localhost:8000/api/v1/modulos/?skip=0&limit=100&activos_only=false`

**Headers:**
```
Authorization: Bearer {token}
```

---

### 👤 Crear Módulo
**POST** `http://localhost:8000/api/v1/modulos/`

**Headers:**
```
Authorization: Bearer {token}
```

**Body:**
```json
{
  "nombre": "Dashboard",
  "descripcion": "Panel principal del sistema",
  "icono": "fas fa-dashboard",
  "ruta": "/dashboard",
  "id_estatus": 1
}
```

---

### 🔍 Obtener Módulo por ID
**GET** `http://localhost:8000/api/v1/modulos/{id_modulo}`

**Headers:**
```
Authorization: Bearer {token}
```

---

### ✏️ Actualizar Módulo
**PUT** `http://localhost:8000/api/v1/modulos/{id_modulo}`

**Headers:**
```
Authorization: Bearer {token}
```

**Body:**
```json
{
  "nombre": "Dashboard Actualizado",
  "descripcion": "Descripción actualizada",
  "icono": "fas fa-chart-line",
  "ruta": "/dashboard-v2",
  "id_estatus": 1
}
```

---

### 🗑️ Eliminar Módulo
**DELETE** `http://localhost:8000/api/v1/modulos/{id_modulo}`

**Headers:**
```
Authorization: Bearer {token}
```

---

### 🔗 Asignar Módulo a Rol
**POST** `http://localhost:8000/api/v1/modulos/asignar-rol`

**Headers:**
```
Authorization: Bearer {token}
```

**Body:**
```json
{
  "modulo_id": 1,
  "rol_id": 1
}
```

---

### 🔓 Desasignar Módulo de Rol
**DELETE** `http://localhost:8000/api/v1/modulos/desasignar-rol?modulo_id=1&rol_id=1`

**Headers:**
```
Authorization: Bearer {token}
```

---

### 🔗 Asignar Múltiples Módulos a Rol
**POST** `http://localhost:8000/api/v1/modulos/asignar-multiples`

**Headers:**
```
Authorization: Bearer {token}
```

**Body:**
```json
{
  "rol_id": 1,
  "modulos_ids": [1, 2, 3, 4]
}
```

---

### 📋 Obtener Módulos por Rol
**GET** `http://localhost:8000/api/v1/modulos/por-rol/{rol_id}`

**Headers:**
```
Authorization: Bearer {token}
```

**Ejemplo:** `http://localhost:8000/api/v1/modulos/por-rol/1`

---

## 4. Clientes

### 📋 Listar Clientes
**GET** `http://localhost:8000/api/v1/clientes/?skip=0&limit=100&activos_only=false`

**Headers:**
```
Authorization: Bearer {token}
```

---

### 👤 Crear Cliente
**POST** `http://localhost:8000/api/v1/clientes/`

**Headers:**
```
Authorization: Bearer {token}
```

**Body:**
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
  "direccion": "Calle Principal 123",
  "pais_id": 1,
  "estado_id": 15,
  "correo_electronico": "cliente@email.com",
  "representante": "Juan Pérez",
  "id_estatus": 1
}
```

---

### 🔍 Obtener Cliente por ID
**GET** `http://localhost:8000/api/v1/clientes/{cliente_id}`

**Headers:**
```
Authorization: Bearer {token}
```

**Ejemplo:** `http://localhost:8000/api/v1/clientes/1`

---

### ✏️ Actualizar Cliente
**PUT** `http://localhost:8000/api/v1/clientes/{cliente_id}`

**Headers:**
```
Authorization: Bearer {token}
```

**Body:** (todos los campos opcionales)
```json
{
  "nombre_razon_social": "Juan Pérez González Actualizado",
  "telefono": "5598765432",
  "direccion": "Nueva Dirección 456",
  "id_estatus": 1
}
```

---

### 🗑️ Eliminar Cliente
**DELETE** `http://localhost:8000/api/v1/clientes/{cliente_id}`

**Headers:**
```
Authorization: Bearer {token}
```

---

### 🔍 Buscar Cliente por RFC
**GET** `http://localhost:8000/api/v1/clientes/buscar/rfc/{rfc}`

**Headers:**
```
Authorization: Bearer {token}
```

**Ejemplo:** `http://localhost:8000/api/v1/clientes/buscar/rfc/PEGJ800101XXX`

---

### ✅ Verificar RFC Disponible
**GET** `http://localhost:8000/api/v1/clientes/verificar-rfc/{rfc}`

**Headers:**
```
Authorization: Bearer {token}
```

**Ejemplo:** `http://localhost:8000/api/v1/clientes/verificar-rfc/PEGJ800101XXX`

**Response:**
```json
{
  "rfc": "PEGJ800101XXX",
  "disponible": false,
  "mensaje": "Ya existe un cliente registrado con el RFC 'PEGJ800101XXX'"
}
```

---

### 🔍 Buscar Clientes por Nombre
**GET** `http://localhost:8000/api/v1/clientes/buscar/nombre?nombre=Juan&skip=0&limit=100`

**Headers:**
```
Authorization: Bearer {token}
```

---

### 📋 Obtener Clientes por Tipo Persona
**GET** `http://localhost:8000/api/v1/clientes/tipo-persona/{tipo_persona}?skip=0&limit=100`

**Headers:**
```
Authorization: Bearer {token}
```

**Ejemplo:** `http://localhost:8000/api/v1/clientes/tipo-persona/1` (1=Física, 2=Moral)

---

### 📋 Obtener Clientes Activos
**GET** `http://localhost:8000/api/v1/clientes/activos?skip=0&limit=100`

**Headers:**
```
Authorization: Bearer {token}
```

---

## 5. Hoteles

### 📋 Listar Hoteles
**GET** `http://localhost:8000/api/v1/hotel/?skip=0&limit=100`

**Headers:**
```
Authorization: Bearer {token}
```

---

### 🏨 Crear Hotel
**POST** `http://localhost:8000/api/v1/hotel/`

**Headers:**
```
Authorization: Bearer {token}
```

**Body:**
```json
{
  "nombre": "Hotel Plaza Madrid",
  "direccion": "Calle Gran Vía, 123, 28013 Madrid",
  "id_pais": 1,
  "id_estado": 15,
  "codigo_postal": "28013",
  "telefono": "+34 91 123 45 67",
  "email_contacto": "reservas@hotelplaza.com",
  "numero_estrellas": 4
}
```

---

### 🔍 Obtener Hotel por ID
**GET** `http://localhost:8000/api/v1/hotel/{hotel_id}`

**Headers:**
```
Authorization: Bearer {token}
```

---

### ✏️ Actualizar Hotel
**PUT** `http://localhost:8000/api/v1/hotel/{hotel_id}`

**Headers:**
```
Authorization: Bearer {token}
```

**Body:**
```json
{
  "nombre": "Hotel Plaza Madrid Actualizado",
  "telefono": "+34 91 999 88 77",
  "numero_estrellas": 5
}
```

---

### 🗑️ Eliminar Hotel
**DELETE** `http://localhost:8000/api/v1/hotel/{hotel_id}`

**Headers:**
```
Authorization: Bearer {token}
```

---

## 6. Tipos de Habitación

### 📋 Listar Tipos de Habitación
**GET** `http://localhost:8000/api/v1/tipo-habitacion/?skip=0&limit=100`

**Headers:**
```
Authorization: Bearer {token}
```

---

### 🛏️ Crear Tipo de Habitación
**POST** `http://localhost:8000/api/v1/tipo-habitacion/`

**Headers:**
```
Authorization: Bearer {token}
```

**Body:**
```json
{
  "tipo_habitacion": "Suite Presidencial",
  "capacidad_personas": 4,
  "numero_camas": 2,
  "descripcion": "Suite de lujo con todas las comodidades",
  "precio_base": 5000.00,
  "estatus_id": 1
}
```

---

### 🔍 Obtener Tipo de Habitación por ID
**GET** `http://localhost:8000/api/v1/tipo-habitacion/{id}`

**Headers:**
```
Authorization: Bearer {token}
```

---

### ✏️ Actualizar Tipo de Habitación
**PUT** `http://localhost:8000/api/v1/tipo-habitacion/{id}`

**Headers:**
```
Authorization: Bearer {token}
```

**Body:**
```json
{
  "tipo_habitacion": "Suite Presidencial Premium",
  "precio_base": 6000.00
}
```

---

### 🗑️ Eliminar Tipo de Habitación
**DELETE** `http://localhost:8000/api/v1/tipo-habitacion/{id}`

**Headers:**
```
Authorization: Bearer {token}
```

---

## 7. Características

### 📋 Listar Características
**GET** `http://localhost:8000/api/v1/caracteristica/?skip=0&limit=100`

**Headers:**
```
Authorization: Bearer {token}
```

---

### ⭐ Crear Característica
**POST** `http://localhost:8000/api/v1/caracteristica/`

**Headers:**
```
Authorization: Bearer {token}
```

**Body:**
```json
{
  "caracteristica": "WiFi Gratis",
  "descripcion": "Conexión WiFi de alta velocidad",
  "estatus_id": 1
}
```

---

### 🔍 Obtener Característica por ID
**GET** `http://localhost:8000/api/v1/caracteristica/{id}`

**Headers:**
```
Authorization: Bearer {token}
```

---

### ✏️ Actualizar Característica
**PUT** `http://localhost:8000/api/v1/caracteristica/{id}`

**Headers:**
```
Authorization: Bearer {token}
```

**Body:**
```json
{
  "caracteristica": "WiFi Premium",
  "descripcion": "Conexión WiFi de ultra alta velocidad"
}
```

---

### 🗑️ Eliminar Característica
**DELETE** `http://localhost:8000/api/v1/caracteristica/{id}`

**Headers:**
```
Authorization: Bearer {token}
```

---

### 🔗 Asignar Característica a Tipo Habitación
**POST** `http://localhost:8000/api/v1/tipo-habitacion-caracteristica/asignar`

**Headers:**
```
Authorization: Bearer {token}
```

**Body:**
```json
{
  "tipo_habitacion_id": 1,
  "caracteristica_id": 1
}
```

---

### 🔓 Desasignar Característica de Tipo Habitación
**DELETE** `http://localhost:8000/api/v1/tipo-habitacion-caracteristica/desasignar?tipo_habitacion_id=1&caracteristica_id=1`

**Headers:**
```
Authorization: Bearer {token}
```

---

## 8. Empleados

### 📋 Listar Empleados
**GET** `http://localhost:8000/api/v1/empleado/?skip=0&limit=100`

**Headers:**
```
Authorization: Bearer {token}
```

---

### 👨‍💼 Crear Empleado
**POST** `http://localhost:8000/api/v1/empleado/`

**Headers:**
```
Authorization: Bearer {token}
```

**Body:**
```json
{
  "clave_empleado": "EMP001",
  "nombre": "María",
  "apellido_paterno": "López",
  "apellido_materno": "García",
  "fecha_nacimiento": "1990-05-15",
  "rfc": "LOGM900515XXX",
  "curp": "LOGM900515MDFPRC01"
}
```

---

### 🔍 Obtener Empleado por ID
**GET** `http://localhost:8000/api/v1/empleado/{id}`

**Headers:**
```
Authorization: Bearer {token}
```

---

### ✏️ Actualizar Empleado
**PUT** `http://localhost:8000/api/v1/empleado/{id}`

**Headers:**
```
Authorization: Bearer {token}
```

---

### 🗑️ Eliminar Empleado
**DELETE** `http://localhost:8000/api/v1/empleado/{id}`

**Headers:**
```
Authorization: Bearer {token}
```

---

## 9. Puestos

### 📋 Listar Puestos
**GET** `http://localhost:8000/api/v1/puesto/?skip=0&limit=100`

**Headers:**
```
Authorization: Bearer {token}
```

---

### 💼 Crear Puesto
**POST** `http://localhost:8000/api/v1/puesto/`

**Headers:**
```
Authorization: Bearer {token}
```

**Body:**
```json
{
  "nombre_puesto": "Recepcionista",
  "descripcion": "Atención al cliente en recepción",
  "salario_base": 8000.00
}
```

---

### 🔍 Obtener Puesto por ID
**GET** `http://localhost:8000/api/v1/puesto/{id}`

**Headers:**
```
Authorization: Bearer {token}
```

---

### ✏️ Actualizar Puesto
**PUT** `http://localhost:8000/api/v1/puesto/{id}`

**Headers:**
```
Authorization: Bearer {token}
```

---

### 🗑️ Eliminar Puesto
**DELETE** `http://localhost:8000/api/v1/puesto/{id}`

**Headers:**
```
Authorization: Bearer {token}
```

---

## 10. Catálogos

### 🌍 Países

#### Listar Países
**GET** `http://localhost:8000/api/v1/pais/?skip=0&limit=100`

**Headers:**
```
Authorization: Bearer {token}
```

#### Crear País
**POST** `http://localhost:8000/api/v1/pais/`

**Headers:**
```
Authorization: Bearer {token}
```

**Body:**
```json
{
  "nombre": "México",
  "id_estatus": 1
}
```

#### Obtener País por ID
**GET** `http://localhost:8000/api/v1/pais/{id}`

#### Actualizar País
**PUT** `http://localhost:8000/api/v1/pais/{id}`

#### Eliminar País
**DELETE** `http://localhost:8000/api/v1/pais/{id}`

---

### 📍 Estados

#### Listar Estados
**GET** `http://localhost:8000/api/v1/estado/?skip=0&limit=100`

**Headers:**
```
Authorization: Bearer {token}
```

#### Listar Estados por País
**GET** `http://localhost:8000/api/v1/estado/pais/{pais_id}`

**Headers:**
```
Authorization: Bearer {token}
```

**Ejemplo:** `http://localhost:8000/api/v1/estado/pais/1`

#### Crear Estado
**POST** `http://localhost:8000/api/v1/estado/`

**Headers:**
```
Authorization: Bearer {token}
```

**Body:**
```json
{
  "nombre": "Ciudad de México",
  "pais_id": 1,
  "id_estatus": 1
}
```

#### Obtener Estado por ID
**GET** `http://localhost:8000/api/v1/estado/{id}`

#### Actualizar Estado
**PUT** `http://localhost:8000/api/v1/estado/{id}`

#### Eliminar Estado
**DELETE** `http://localhost:8000/api/v1/estado/{id}`

---

## 11. Email

### 📧 Enviar Email Básico
**POST** `http://localhost:8000/api/v1/email/enviar`

**Headers:**
```
Authorization: Bearer {token}
```

**Body:**
```json
{
  "destinatario": "cliente@email.com",
  "asunto": "Confirmación de Reserva",
  "cuerpo": "Su reserva ha sido confirmada"
}
```

---

### 📧 Enviar Email con Template
**POST** `http://localhost:8000/api/v1/email/enviar-template`

**Headers:**
```
Authorization: Bearer {token}
```

**Body:**
```json
{
  "destinatario": "cliente@email.com",
  "asunto": "Confirmación de Reserva",
  "template_nombre": "confirmacion_reserva",
  "variables": {
    "nombre_cliente": "Juan Pérez",
    "numero_reserva": "RES-001",
    "fecha_entrada": "2024-02-01",
    "fecha_salida": "2024-02-05"
  }
}
```

---

### 📋 Obtener Historial de Emails
**GET** `http://localhost:8000/api/v1/email/historial?skip=0&limit=100`

**Headers:**
```
Authorization: Bearer {token}
```

---

## 📝 Notas Importantes

### Autenticación
- Todos los endpoints (excepto `/login`, `/verificar-disponibilidad` y `/registro-cliente`) requieren token JWT
- El token se obtiene del endpoint de login
- El token debe enviarse en el header `Authorization: Bearer {token}`
- El token expira en 30 minutos

### Códigos de Respuesta HTTP
- `200 OK` - Solicitud exitosa
- `201 Created` - Recurso creado exitosamente
- `204 No Content` - Eliminación exitosa
- `400 Bad Request` - Datos inválidos
- `401 Unauthorized` - No autenticado o token inválido
- `404 Not Found` - Recurso no encontrado
- `500 Internal Server Error` - Error del servidor

### Paginación
- La mayoría de los endpoints de listado soportan paginación mediante `skip` y `limit`
- `skip` = número de registros a omitir (por defecto 0)
- `limit` = número máximo de registros a retornar (por defecto 100, máximo 1000)

### Validaciones RFC
- El RFC es único en la tabla de clientes
- Se valida el formato al crear/actualizar
- Endpoint específico para verificar disponibilidad

### Password Temporal
- Se genera automáticamente si no se proporciona password en registro de cliente
- Expira en 7 días
- Debe cambiarse en el primer login
- El login retorna información si tiene password temporal activa

---

**Última actualización:** 2024-01-15  
**Versión:** 1.0.0

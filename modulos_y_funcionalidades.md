# Módulos y Funcionalidades del Sistema InnPulse360

## Índice
1. [Módulo de Seguridad y Autenticación](#1-módulo-de-seguridad-y-autenticación)
2. [Módulo de Hoteles](#2-módulo-de-hoteles)
3. [Módulo de Clientes](#3-módulo-de-clientes)
4. [Módulo de Reservaciones](#4-módulo-de-reservaciones)
5. [Módulo de Empleados](#5-módulo-de-empleados)
6. [Módulo de Limpieza (Camarista)](#6-módulo-de-limpieza-camarista)
7. [Módulo de Mantenimiento](#7-módulo-de-mantenimiento)
8. [Módulo de Catálogos](#8-módulo-de-catálogos)
9. [Módulo de Email](#9-módulo-de-email)
10. [Módulo de Almacenamiento](#10-módulo-de-almacenamiento)
11. [Utilidades del Sistema](#11-utilidades-del-sistema)

---

## 1. Módulo de Seguridad y Autenticación

### 1.1. Gestión de Usuarios (`routes_usuario.py`)

**Endpoints disponibles:**

#### Autenticación
- **POST** `/api/v1/usuarios/login`
  - **Descripción**: Iniciar sesión de usuario
  - **Parámetros**: `login`, `password`
  - **Respuesta**: Token JWT válido por 30 minutos
  - **Autenticación**: No requerida

#### CRUD de Usuarios
- **POST** `/api/v1/usuarios/`
  - **Descripción**: Crear un nuevo usuario
  - **Parámetros**: `login`, `correo_electronico`, `password`, `estatus_id`
  - **Autenticación**: Requerida
  - **Funcionalidad**: Encripta automáticamente la contraseña antes de guardarla

- **GET** `/api/v1/usuarios/`
  - **Descripción**: Listar todos los usuarios con paginación
  - **Parámetros Query**: `skip` (default: 0), `limit` (default: 100)
  - **Autenticación**: Requerida

- **GET** `/api/v1/usuarios/{id_usuario}`
  - **Descripción**: Obtener usuario por ID
  - **Autenticación**: Requerida

- **GET** `/api/v1/usuarios/login/{login}`
  - **Descripción**: Obtener usuario por login
  - **Autenticación**: Requerida

- **PUT** `/api/v1/usuarios/{id_usuario}`
  - **Descripción**: Actualizar usuario (actualización parcial)
  - **Parámetros**: Todos opcionales (`login`, `correo_electronico`, `password`, `estatus_id`)
  - **Autenticación**: Requerida
  - **Funcionalidad**: Si se proporciona nueva contraseña, se encripta automáticamente

- **DELETE** `/api/v1/usuarios/{id_usuario}`
  - **Descripción**: Eliminar usuario (eliminación lógica)
  - **Autenticación**: Requerida
  - **Funcionalidad**: Cambia el estatus a inactivo, no elimina físicamente

#### Perfil de Usuario
- **GET** `/api/v1/usuarios/me/profile`
  - **Descripción**: Obtener perfil del usuario autenticado
  - **Autenticación**: Requerida
  - **Funcionalidad**: Retorna información basada en el token JWT

- **PUT** `/api/v1/usuarios/me/profile`
  - **Descripción**: Actualizar perfil del usuario autenticado
  - **Autenticación**: Requerida

#### Registro de Clientes
- **POST** `/api/v1/usuarios/verificar-disponibilidad`
  - **Descripción**: Verificar disponibilidad de login y correo para registro
  - **Parámetros**: `login`, `correo_electronico`
  - **Autenticación**: No requerida
  - **Respuesta**: Indica si login y correo están disponibles

- **POST** `/api/v1/usuarios/registro-cliente`
  - **Descripción**: Registrar nuevo usuario asociado a un cliente
  - **Parámetros**: `login`, `correo_electronico`, `password` (opcional), `cliente_id`
  - **Autenticación**: No requerida
  - **Funcionalidad**: Si no se proporciona password, se genera uno temporal

- **POST** `/api/v1/usuarios/cambiar-password-temporal`
  - **Descripción**: Cambiar contraseña temporal por una definitiva
  - **Parámetros**: `login`, `password_actual`, `password_nueva`, `password_confirmacion`
  - **Autenticación**: No requerida

**Servicios relacionados:**
- `services/seguridad/usuario_service.py`: Lógica de negocio de usuarios
- `dao/seguridad/dao_usuario.py`: Acceso a datos de usuarios
- `utils/generacion_token.py`: Generación de tokens JWT
- `utils/password_generator.py`: Generación de contraseñas temporales

### 1.2. Gestión de Roles (`routes_roles.py`)

**Endpoints disponibles:**
- CRUD completo de roles
- Asignación de permisos a roles
- Consulta de roles disponibles

**Funcionalidad**: Sistema de roles y permisos para control de acceso basado en roles (RBAC).

### 1.3. Gestión de Usuario-Rol (`routes_usuario_rol.py`)

**Endpoints disponibles:**
- Asignar roles a usuarios
- Remover roles de usuarios
- Consultar roles de un usuario específico

**Funcionalidad**: Permite asignar múltiples roles a un usuario para control de acceso granular.

### 1.4. Gestión de Módulos (`routes_modulos.py`)

**Endpoints disponibles:**
- CRUD de módulos del sistema
- Asignación de módulos a roles
- Consulta de módulos disponibles

**Funcionalidad**: Define los módulos del sistema y sus permisos asociados.

---

## 2. Módulo de Hoteles

### 2.1. Gestión de Hoteles (`routes_hotel.py`)

**Endpoints disponibles:**

- **GET** `/api/v1/hotel/`
  - **Descripción**: Listar todos los hoteles con paginación
  - **Parámetros Query**: `skip` (default: 0), `limit` (default: 100, max: 1000)
  - **Autenticación**: Requerida

- **GET** `/api/v1/hotel/{hotel_id}`
  - **Descripción**: Obtener hotel específico por ID
  - **Autenticación**: Requerida

- **POST** `/api/v1/hotel/`
  - **Descripción**: Crear nuevo hotel
  - **Parámetros**: `nombre`, `direccion`, `id_estado`, `id_pais`, `codigo_postal`, `telefono`, `email_contacto`, `numero_estrellas`
  - **Autenticación**: Requerida
  - **Status Code**: 201 Created

- **PUT** `/api/v1/hotel/{hotel_id}`
  - **Descripción**: Actualizar hotel (actualización parcial)
  - **Autenticación**: Requerida

- **DELETE** `/api/v1/hotel/{hotel_id}`
  - **Descripción**: Eliminar hotel
  - **Autenticación**: Requerida
  - **Status Code**: 204 No Content

#### Búsquedas Especializadas
- **GET** `/api/v1/hotel/buscar/nombre/{nombre}`
  - **Descripción**: Buscar hoteles por nombre (búsqueda parcial)
  - **Autenticación**: Requerida

- **GET** `/api/v1/hotel/pais/{id_pais}`
  - **Descripción**: Obtener todos los hoteles de un país
  - **Autenticación**: Requerida

- **GET** `/api/v1/hotel/estrellas/{numero_estrellas}`
  - **Descripción**: Obtener hoteles por número de estrellas (1-5)
  - **Autenticación**: Requerida
  - **Validación**: Número de estrellas debe estar entre 1 y 5

**Funcionalidades especiales:**
- Construcción automática de URLs de fotos de perfil desde Supabase Storage
- Validación de datos de entrada
- Manejo de relaciones con países y estados

**Servicios relacionados:**
- `services/hotel/hotel_service.py`: Lógica de negocio de hoteles
- `dao/hotel/dao_hotel.py`: Acceso a datos de hoteles
- `services/storage/hotel_storage_service.py`: Gestión de imágenes de hoteles

### 2.2. Gestión de Tipos de Habitación (`routes_tipo_habitacion.py`)

**Endpoints disponibles:**
- CRUD completo de tipos de habitación
- Consulta de tipos de habitación por hotel
- Gestión de características asociadas

**Funcionalidad**: Define los diferentes tipos de habitaciones disponibles en los hoteles (Suite, Estándar, Deluxe, etc.).

### 2.3. Gestión de Características (`routes_caracteristica.py`)

**Endpoints disponibles:**
- CRUD de características de habitaciones
- Asignación de características a tipos de habitación

**Funcionalidad**: Define características de habitaciones (WiFi, TV, Aire Acondicionado, etc.).

### 2.4. Gestión de Tipo Habitación-Característica (`routes_tipo_habitacion_caracteristica.py`)

**Endpoints disponibles:**
- Asignar características a tipos de habitación
- Remover características de tipos de habitación
- Consultar características de un tipo de habitación

**Funcionalidad**: Relación muchos a muchos entre tipos de habitación y características.

### 2.5. Gestión de Pisos (`routes_piso.py`)

**Endpoints disponibles:**
- CRUD de pisos
- Consulta de pisos por hotel

**Funcionalidad**: Gestión de pisos de los hoteles.

### 2.6. Gestión de Áreas de Habitación (`routes_habitacion_area.py`)

**Endpoints disponibles:**
- CRUD de áreas/habitaciones
- Consulta de habitaciones por piso
- Consulta de habitaciones por tipo
- Consulta de habitaciones por hotel

**Funcionalidad**: Gestión de las habitaciones físicas del hotel con su ubicación y tipo.

### 2.7. Gestión de Imágenes de Hoteles (`routes_hotel_imagenes.py`)

**Endpoints disponibles:**
- Subir imágenes de hoteles
- Eliminar imágenes de hoteles
- Listar imágenes de un hotel
- Obtener URL pública de imágenes

**Funcionalidad**: Gestión de imágenes de hoteles almacenadas en Supabase Storage.

### 2.8. Gestión de Imágenes de Habitaciones (`routes_habitacion_imagenes.py`)

**Endpoints disponibles:**
- Subir imágenes de habitaciones
- Eliminar imágenes de habitaciones
- Listar imágenes de una habitación

**Funcionalidad**: Gestión de imágenes de habitaciones en Supabase Storage.

### 2.9. Gestión de Imágenes de Tipos de Habitación (`routes_tipo_habitacion_imagenes.py`)

**Endpoints disponibles:**
- Subir imágenes de tipos de habitación
- Eliminar imágenes
- Listar imágenes de un tipo de habitación

**Funcionalidad**: Gestión de imágenes representativas de tipos de habitación.

---

## 3. Módulo de Clientes

### 3.1. Gestión de Clientes (`routes_cliente.py`)

**Endpoints disponibles:**
- CRUD completo de clientes
- Búsqueda de clientes por nombre
- Búsqueda de clientes por correo electrónico
- Consulta de reservaciones de un cliente

**Funcionalidad**: Gestión completa de información de clientes, incluyendo datos personales, contacto y preferencias.

**Servicios relacionados:**
- `services/cliente/cliente_service.py`: Lógica de negocio de clientes
- `dao/cliente/dao_cliente.py`: Acceso a datos de clientes

---

## 4. Módulo de Reservaciones

### 4.1. Gestión de Reservaciones (`routes_reservacion.py`)

**Endpoints disponibles:**

- **GET** `/api/v1/reservaciones/`
  - **Descripción**: Listar todas las reservaciones
  - **Autenticación**: Requerida

- **GET** `/api/v1/reservaciones/{id_reservacion}`
  - **Descripción**: Obtener reservación específica por ID
  - **Autenticación**: Requerida

- **GET** `/api/v1/reservaciones/cliente/{id_cliente}`
  - **Descripción**: Obtener reservaciones de un cliente específico
  - **Autenticación**: Requerida

- **GET** `/api/v1/reservaciones/habitacion/{habitacion_area_id}`
  - **Descripción**: Obtener reservaciones de una habitación específica
  - **Autenticación**: Requerida

- **GET** `/api/v1/reservaciones/fechas/`
  - **Descripción**: Obtener reservaciones por rango de fechas
  - **Parámetros Query**: `fecha_inicio`, `fecha_fin`
  - **Autenticación**: Requerida

- **POST** `/api/v1/reservaciones/`
  - **Descripción**: Crear nueva reservación
  - **Autenticación**: Requerida

- **PUT** `/api/v1/reservaciones/{id_reservacion}`
  - **Descripción**: Actualizar reservación
  - **Autenticación**: Requerida

- **DELETE** `/api/v1/reservaciones/{id_reservacion}`
  - **Descripción**: Eliminar reservación
  - **Autenticación**: Requerida

**Funcionalidad**: Gestión completa del ciclo de vida de reservaciones, incluyendo creación, modificación, consulta y cancelación.

**Servicios relacionados:**
- `services/reserva/reservacion_service.py`: Lógica de negocio de reservaciones
- `dao/reserva/dao_reservacion.py`: Acceso a datos de reservaciones

### 4.2. Gestión de Tipos de Cargo (`routes_tipo_cargo.py`)

**Endpoints disponibles:**
- CRUD de tipos de cargo
- Consulta de tipos de cargo disponibles

**Funcionalidad**: Define los tipos de cargo adicionales que se pueden agregar a una reservación (desayuno, cena, spa, etc.).

### 4.3. Gestión de Cargos (`routes_cargo.py`)

**Endpoints disponibles:**
- CRUD de cargos
- Asociar cargos a reservaciones
- Consulta de cargos por reservación

**Funcionalidad**: Gestión de cargos adicionales asociados a reservaciones.

### 4.4. Gestión de Servicios de Transporte (`routes_servicio_transporte.py`)

**Endpoints disponibles:**
- CRUD de servicios de transporte
- Consulta de servicios disponibles

**Funcionalidad**: Define los servicios de transporte disponibles (aeropuerto, estación, etc.).

### 4.5. Gestión de Cargo-Servicio Transporte (`routes_cargo_servicio_transporte.py`)

**Endpoints disponibles:**
- Asociar servicios de transporte a cargos
- Consulta de servicios de transporte por cargo

**Funcionalidad**: Relación entre cargos y servicios de transporte.

---

## 5. Módulo de Empleados

### 5.1. Gestión de Empleados (`routes_empleado.py`)

**Endpoints disponibles:**
- CRUD completo de empleados
- Consulta de empleados por puesto
- Consulta de empleados por hotel
- Gestión de direcciones de empleados

**Funcionalidad**: Gestión completa de información de empleados, incluyendo datos personales, contacto, dirección y puesto.

**Servicios relacionados:**
- `services/empleado/empleado_service.py`: Lógica de negocio de empleados
- `dao/empleado/dao_empleado.py`: Acceso a datos de empleados
- `dao/empleado/dao_direccion.py`: Acceso a datos de direcciones

### 5.2. Gestión de Puestos (`routes_puesto.py`)

**Endpoints disponibles:**
- CRUD de puestos de trabajo
- Consulta de puestos disponibles

**Funcionalidad**: Define los diferentes puestos de trabajo en el hotel (Recepcionista, Camarista, Mantenimiento, etc.).

---

## 6. Módulo de Limpieza (Camarista)

### 6.1. Gestión de Limpiezas (`routes_limpieza.py`)

**Endpoints disponibles:**

- **GET** `/api/v1/limpiezas/`
  - **Descripción**: Listar todas las limpiezas
  - **Autenticación**: Requerida

- **GET** `/api/v1/limpiezas/{id_limpieza}`
  - **Descripción**: Obtener limpieza específica por ID
  - **Autenticación**: Requerida

- **POST** `/api/v1/limpiezas/`
  - **Descripción**: Crear nueva limpieza
  - **Autenticación**: Requerida

- **PUT** `/api/v1/limpiezas/{id_limpieza}`
  - **Descripción**: Actualizar limpieza
  - **Autenticación**: Requerida

- **DELETE** `/api/v1/limpiezas/{id_limpieza}`
  - **Descripción**: Eliminar limpieza (marcar como eliminada, estatus_id = 4)
  - **Autenticación**: Requerida
  - **Funcionalidad**: Eliminación lógica, no física

- **GET** `/api/v1/limpiezas/empleado/{empleado_id}`
  - **Descripción**: Obtener limpiezas asignadas a un empleado
  - **Autenticación**: Requerida

- **GET** `/api/v1/limpiezas/habitacion-area/{habitacion_area_id}`
  - **Descripción**: Obtener limpiezas de una habitación específica
  - **Autenticación**: Requerida

- **GET** `/api/v1/limpiezas/fecha/`
  - **Descripción**: Obtener limpiezas por fecha
  - **Parámetros Query**: `fecha` (datetime)
  - **Autenticación**: Requerida

**Funcionalidad**: Gestión completa del proceso de limpieza de habitaciones, incluyendo asignación a empleados, seguimiento de estatus y registro de fechas.

**Servicios relacionados:**
- `services/camarista/limpieza_service.py`: Lógica de negocio de limpiezas
- `dao/camarista/dao_limpieza.py`: Acceso a datos de limpiezas

### 6.2. Gestión de Tipos de Limpieza (`routes_tipo_limpieza.py`)

**Endpoints disponibles:**
- CRUD de tipos de limpieza
- Consulta de tipos disponibles

**Funcionalidad**: Define los diferentes tipos de limpieza (Limpieza Normal, Limpieza Profunda, Limpieza Post-Checkout, etc.).

### 6.3. Gestión de Estatus de Limpieza (`routes_estatus_limpieza.py`)

**Endpoints disponibles:**
- CRUD de estatus de limpieza
- Consulta de estatus disponibles

**Funcionalidad**: Define los diferentes estatus de una limpieza (Pendiente, En Proceso, Completada, Cancelada, etc.).

### 6.4. Gestión de Imágenes de Limpieza (`routes_limpieza_imagenes.py`)

**Endpoints disponibles:**
- Subir imágenes de limpieza
- Eliminar imágenes
- Listar imágenes de una limpieza

**Funcionalidad**: Gestión de evidencias fotográficas de limpiezas almacenadas en Supabase Storage.

---

## 7. Módulo de Mantenimiento

### 7.1. Gestión de Mantenimientos (`routes_mantenimiento.py`)

**Endpoints disponibles:**

- **GET** `/api/v1/mantenimientos/`
  - **Descripción**: Listar todos los mantenimientos
  - **Autenticación**: Requerida

- **GET** `/api/v1/mantenimientos/{id_mantenimiento}`
  - **Descripción**: Obtener mantenimiento específico por ID
  - **Autenticación**: Requerida

- **POST** `/api/v1/mantenimientos/`
  - **Descripción**: Crear nuevo mantenimiento
  - **Autenticación**: Requerida

- **PUT** `/api/v1/mantenimientos/{id_mantenimiento}`
  - **Descripción**: Actualizar mantenimiento
  - **Autenticación**: Requerida

- **DELETE** `/api/v1/mantenimientos/{id_mantenimiento}`
  - **Descripción**: Eliminar mantenimiento
  - **Autenticación**: Requerida

- **GET** `/api/v1/mantenimientos/fecha/`
  - **Descripción**: Obtener mantenimientos por fecha
  - **Parámetros Query**: `fecha_inicio` (datetime)
  - **Autenticación**: Requerida

- **GET** `/api/v1/mantenimientos/habitacion-area/{habitacion_area_id}`
  - **Descripción**: Obtener mantenimientos de una habitación específica
  - **Autenticación**: Requerida

- **GET** `/api/v1/mantenimientos/empleado/{empleado_id}`
  - **Descripción**: Obtener mantenimientos asignados a un empleado
  - **Autenticación**: Requerida

**Funcionalidad**: Gestión completa del proceso de mantenimiento de habitaciones y áreas del hotel, incluyendo programación, asignación y seguimiento.

**Servicios relacionados:**
- `services/mantenimiento/mantenimiento_service.py`: Lógica de negocio de mantenimientos
- `dao/mantenimiento/dao_mantenimiento.py`: Acceso a datos de mantenimientos

### 7.2. Gestión de Incidencias (`routes_incidencia.py`)

**Endpoints disponibles:**
- CRUD completo de incidencias
- Consulta de incidencias por habitación
- Consulta de incidencias por estatus
- Asociación de incidencias a mantenimientos

**Funcionalidad**: Registro y seguimiento de incidencias reportadas en habitaciones o áreas del hotel.

**Servicios relacionados:**
- `services/mantenimiento/incidencia_service.py`: Lógica de negocio de incidencias
- `dao/mantenimiento/dao_incidencia.py`: Acceso a datos de incidencias

### 7.3. Gestión de Imágenes de Mantenimiento (`routes_mantenimiento_imagenes.py`)

**Endpoints disponibles:**
- Subir imágenes de mantenimiento
- Eliminar imágenes
- Listar imágenes de un mantenimiento

**Funcionalidad**: Gestión de evidencias fotográficas de mantenimientos.

### 7.4. Gestión de Imágenes de Incidencias (`routes_incidencia_imagenes.py`)

**Endpoints disponibles:**
- Subir imágenes de incidencias
- Eliminar imágenes
- Listar imágenes de una incidencia

**Funcionalidad**: Gestión de evidencias fotográficas de incidencias reportadas.

---

## 8. Módulo de Catálogos

### 8.1. Gestión de Países (`routes_pais.py`)

**Endpoints disponibles:**
- CRUD de países
- Consulta de países disponibles
- Búsqueda de países por nombre

**Funcionalidad**: Catálogo maestro de países para uso en hoteles y clientes.

**Servicios relacionados:**
- `services/catalogos/pais_service.py`: Lógica de negocio de países
- `dao/catalogos/dao_pais.py`: Acceso a datos de países

### 8.2. Gestión de Estados (`routes_estado.py`)

**Endpoints disponibles:**
- CRUD de estados
- Consulta de estados por país
- Consulta de estados disponibles

**Funcionalidad**: Catálogo maestro de estados/provincias asociados a países.

**Servicios relacionados:**
- `services/catalogos/estado_service.py`: Lógica de negocio de estados
- `dao/catalogos/dao_estado.py`: Acceso a datos de estados

### 8.3. Gestión de Periodicidad (`routes_periodicidad.py`)

**Endpoints disponibles:**
- CRUD de periodicidades
- Consulta de periodicidades disponibles

**Funcionalidad**: Define las periodicidades para mantenimientos programados (Diario, Semanal, Mensual, etc.).

**Servicios relacionados:**
- `services/catalogos/periodicidad_service.py`: Lógica de negocio de periodicidades
- `dao/catalogos/dao_periodicidad.py`: Acceso a datos de periodicidades

---

## 9. Módulo de Email

### 9.1. Envío de Emails (`routes_email.py`)

**Endpoints disponibles:**

- **POST** `/api/v1/emails/send`
  - **Descripción**: Enviar email básico (útil para testing)
  - **Parámetros**: `destinatario_email`, `asunto`, `contenido_html`
  - **Autenticación**: No requerida (para testing)
  - **Funcionalidad**: Envía email usando configuración SMTP

- **GET** `/api/v1/emails/logs`
  - **Descripción**: Consultar logs de emails enviados
  - **Parámetros Query**: `skip`, `limit`, `destinatario_email` (opcional), `estado` (opcional)
  - **Autenticación**: Requerida
  - **Funcionalidad**: Retorna historial de emails con filtros opcionales

- **GET** `/api/v1/emails/logs/{id_log}`
  - **Descripción**: Obtener log específico de email
  - **Autenticación**: Requerida

- **GET** `/api/v1/emails/templates`
  - **Descripción**: Listar plantillas de email disponibles
  - **Autenticación**: Requerida

- **GET** `/api/v1/emails/templates/{id_template}`
  - **Descripción**: Obtener plantilla específica
  - **Autenticación**: Requerida

**Funcionalidades:**
- Envío de emails HTML con plantillas personalizables
- Sistema de logging de todos los emails enviados
- Plantillas predefinidas (bienvenida, reset de contraseña, notificaciones, etc.)
- Configuración SMTP flexible (Gmail, Outlook, etc.)
- Branding personalizado con colores de InnPulse360

**Servicios relacionados:**
- `services/email/email_service.py`: Lógica de negocio de emails
- `services/email/template_service.py`: Gestión de plantillas
- `dao/email/dao_email_log.py`: Acceso a logs de emails
- `dao/email/dao_email_template.py`: Acceso a plantillas
- `core/email_config.py`: Configuración de email

---

## 10. Módulo de Almacenamiento

### 10.1. Gestión General de Imágenes (`routes_imagenes.py`)

**Endpoints disponibles:**
- Subir imágenes genéricas
- Eliminar imágenes
- Obtener URL pública de imágenes
- Listar imágenes

**Funcionalidad**: Servicio genérico para gestión de imágenes en Supabase Storage.

### 10.2. Servicios de Almacenamiento Especializados

El sistema incluye servicios especializados para diferentes tipos de almacenamiento:

#### Hotel Storage Service
- Gestión de imágenes de hoteles
- Organización por hotel
- Generación de URLs públicas

#### Habitación Storage Service
- Gestión de imágenes de habitaciones
- Organización por habitación
- Múltiples imágenes por habitación

#### Limpieza Storage Service
- Gestión de evidencias fotográficas de limpiezas
- Organización por limpieza

#### Mantenimiento Storage Service
- Gestión de evidencias fotográficas de mantenimientos
- Organización por mantenimiento

#### Incidencia Storage Service
- Gestión de evidencias fotográficas de incidencias
- Organización por incidencia

#### Tipo Habitación Storage Service
- Gestión de imágenes representativas de tipos de habitación
- Organización por tipo de habitación

#### PDF Storage Service
- Gestión de documentos PDF
- Almacenamiento en bucket separado
- Generación de URLs públicas

**Características del sistema de almacenamiento:**
- Almacenamiento en Supabase Storage
- Buckets separados para imágenes y PDFs
- URLs públicas generadas automáticamente
- Organización jerárquica por tipo de entidad
- Soporte para múltiples archivos por entidad

**Servicios relacionados:**
- `services/storage/base_storage_service.py`: Servicio base de almacenamiento
- `services/storage/image_storage_service.py`: Servicio de imágenes
- `services/storage/pdf_storage_service.py`: Servicio de PDFs
- `core/supabase_client.py`: Cliente Supabase (Singleton)

---

## 11. Utilidades del Sistema

### 11.1. Generación de Tokens (`utils/generacion_token.py`)

**Funcionalidad:**
- Generación de tokens JWT para autenticación
- Configuración de expiración de tokens
- Validación de tokens

### 11.2. Generación de Contraseñas (`utils/password_generator.py`)

**Funciones disponibles:**

- `generar_password_temporal(longitud=12)`
  - Genera contraseña temporal segura
  - Incluye mayúsculas, minúsculas y números
  - Mínimo 8 caracteres

- `generar_password_compleja(longitud=16)`
  - Genera contraseña compleja con símbolos especiales
  - Incluye mayúsculas, minúsculas, números y símbolos
  - Mínimo 12 caracteres

- `validar_fortaleza_password(password)`
  - Valida la fortaleza de una contraseña
  - Requisitos: mínimo 6 caracteres, al menos una mayúscula, una minúscula y un número
  - Retorna tupla (es_valida, mensaje)

**Funcionalidad**: Utilidades para generar y validar contraseñas seguras.

### 11.3. Rutas de Imágenes (`utils/rutas_imagenes.py`)

**Funcionalidad:**
- Generación de rutas estructuradas para almacenamiento de imágenes
- Organización jerárquica de archivos
- Validación de rutas

---

## Resumen de Funcionalidades por Módulo

### Módulo de Seguridad
- ✅ Autenticación con JWT
- ✅ Gestión de usuarios (CRUD completo)
- ✅ Sistema de roles y permisos (RBAC)
- ✅ Registro de clientes con generación de contraseñas temporales
- ✅ Cambio de contraseñas temporales
- ✅ Perfil de usuario

### Módulo de Hoteles
- ✅ CRUD completo de hoteles
- ✅ Búsquedas especializadas (por nombre, país, estrellas)
- ✅ Gestión de tipos de habitación
- ✅ Gestión de características de habitaciones
- ✅ Gestión de pisos y áreas de habitación
- ✅ Gestión de imágenes de hoteles, habitaciones y tipos

### Módulo de Clientes
- ✅ CRUD completo de clientes
- ✅ Búsquedas por nombre y correo
- ✅ Consulta de reservaciones de clientes

### Módulo de Reservaciones
- ✅ CRUD completo de reservaciones
- ✅ Consultas por cliente, habitación y fechas
- ✅ Gestión de cargos adicionales
- ✅ Gestión de servicios de transporte
- ✅ Asociación de servicios de transporte a cargos

### Módulo de Empleados
- ✅ CRUD completo de empleados
- ✅ Gestión de direcciones de empleados
- ✅ Gestión de puestos de trabajo
- ✅ Consultas por puesto y hotel

### Módulo de Limpieza
- ✅ CRUD completo de limpiezas
- ✅ Consultas por empleado, habitación y fecha
- ✅ Gestión de tipos de limpieza
- ✅ Gestión de estatus de limpieza
- ✅ Gestión de imágenes de limpieza

### Módulo de Mantenimiento
- ✅ CRUD completo de mantenimientos
- ✅ Consultas por fecha, habitación y empleado
- ✅ Gestión de incidencias
- ✅ Asociación de incidencias a mantenimientos
- ✅ Gestión de imágenes de mantenimiento e incidencias

### Módulo de Catálogos
- ✅ Gestión de países
- ✅ Gestión de estados
- ✅ Gestión de periodicidades

### Módulo de Email
- ✅ Envío de emails HTML
- ✅ Sistema de logging de emails
- ✅ Plantillas personalizables
- ✅ Configuración SMTP flexible

### Módulo de Almacenamiento
- ✅ Almacenamiento en Supabase Storage
- ✅ Gestión de imágenes por tipo de entidad
- ✅ Gestión de PDFs
- ✅ Generación automática de URLs públicas

---

## Estadísticas del Sistema

- **Total de Endpoints**: 100+ endpoints REST
- **Módulos Principales**: 11 módulos
- **Autenticación**: JWT Bearer Token
- **Base de Datos**: SQL Server (MSSQL)
- **Almacenamiento**: Supabase Storage
- **Framework**: FastAPI 0.104.1
- **ORM**: SQLAlchemy 2.0.23

---

**Última actualización**: Diciembre 2024
**Versión del Sistema**: 1.0.0


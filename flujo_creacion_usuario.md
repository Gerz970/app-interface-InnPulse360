# Flujo de Creación de Usuario y Acceso a la Plataforma - InnPulse360

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Flujo 1: Creación de Usuario por Administrador](#flujo-1-creación-de-usuario-por-administrador)
3. [Flujo 2: Registro de Cliente (Autoregistro)](#flujo-2-registro-de-cliente-autoregistro)
4. [Flujo 3: Iniciar Sesión](#flujo-3-iniciar-sesión-acceso-a-la-plataforma)
5. [Resumen del Flujo Completo](#resumen-del-flujo-completo)
6. [Estado Actual en la App Móvil](#estado-actual-en-la-app-móvil)
7. [Diagramas de Flujo](#diagramas-de-flujo)
8. [Ejemplos de Código](#ejemplos-de-código)

---

## Introducción

El sistema InnPulse360 tiene **dos flujos principales** para crear usuarios:

1. **Creación de usuario por administrador** (requiere autenticación)
2. **Registro de cliente** (sin autenticación, para clientes existentes)

Ambos flujos terminan con el mismo proceso de autenticación para acceder a la plataforma.

---

## Flujo 1: Creación de Usuario por Administrador

### Descripción

Permite a un administrador crear usuarios directamente en el sistema. Requiere autenticación y permisos de administrador.

### Endpoint

```
POST /api/v1/usuarios/
```

### Autenticación

- **Requerida**: Sí (Bearer Token)
- **Permisos**: Usuario administrador

### Datos Requeridos

```json
{
  "login": "nuevo.usuario",
  "correo_electronico": "usuario@email.com",
  "password": "Password123",
  "estatus_id": 1,
  "roles_ids": [1, 2]
}
```

**Campos:**
- `login` (string, requerido): Login único del usuario (máximo 25 caracteres)
- `correo_electronico` (string, requerido): Email único del usuario (máximo 50 caracteres)
- `password` (string, requerido): Contraseña (mínimo 6 caracteres, se encripta automáticamente)
- `estatus_id` (integer, opcional): Estatus del usuario (1=Activo por defecto)
- `roles_ids` (array, opcional): Lista de IDs de roles a asignar

### Proceso Interno

1. **Validación de unicidad**
   - Verifica que el `login` no exista
   - Verifica que el `correo_electronico` no exista

2. **Validación de roles** (si se proporcionan)
   - Verifica que todos los roles existan y estén activos

3. **Encriptación de contraseña**
   - La contraseña se encripta usando **Argon2** antes de guardarse

4. **Creación del usuario**
   - Se crea el registro en la base de datos

5. **Asignación de foto de perfil**
   - Si no se proporciona, se asigna una foto por defecto: `usuarios/perfil/default.jpg`

6. **Asignación de roles**
   - Si se proporcionaron `roles_ids`, se asignan al usuario

### Respuesta Exitosa (201 Created)

```json
{
  "id_usuario": 5,
  "login": "nuevo.usuario",
  "correo_electronico": "usuario@email.com",
  "estatus_id": 1,
  "roles": [
    {
      "id_rol": 1,
      "rol": "Administrador"
    }
  ],
  "url_foto_perfil": "https://innpulse360.supabase.co/storage/v1/object/public/images/usuarios/perfil/default.jpg"
}
```

### Errores Posibles

- `400 Bad Request`: Login o email ya existe
- `401 Unauthorized`: Token inválido o ausente
- `400 Bad Request`: Rol con ID X no encontrado o inactivo

### Ejemplo cURL

```bash
curl -X POST "https://app-interface-innpulse360-production.up.railway.app/api/v1/usuarios/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "login": "nuevo.usuario",
    "correo_electronico": "usuario@email.com",
    "password": "Password123",
    "estatus_id": 1,
    "roles_ids": [1]
  }'
```

### Acceso Después de Crear

Una vez creado el usuario, puede iniciar sesión inmediatamente usando:
- **Login**: El `login` proporcionado
- **Password**: La contraseña proporcionada (antes de encriptarse)

---

## Flujo 2: Registro de Cliente (Autoregistro)

### Descripción

Permite que un cliente existente en la base de datos se registre como usuario del sistema. Este flujo **no requiere autenticación previa**, pero el cliente debe existir previamente en la tabla de clientes.

### Paso 1: Verificar Disponibilidad

#### Endpoint

```
POST /api/v1/usuarios/verificar-disponibilidad
```

#### Autenticación

- **Requerida**: No

#### Datos Requeridos

```json
{
  "login": "cliente123",
  "correo_electronico": "cliente@email.com"
}
```

**Campos:**
- `login` (string, requerido): Login a verificar (máximo 25 caracteres)
- `correo_electronico` (string, requerido): Correo a verificar (máximo 50 caracteres)

#### Proceso Interno

1. **Verificación de login**
   - Verifica si el `login` ya existe en la tabla de usuarios
   - `login_disponible = true` si no existe

2. **Búsqueda de cliente**
   - Busca un cliente con el `correo_electronico` proporcionado
   - `correo_en_clientes = true` si existe

3. **Validación combinada**
   - `puede_registrar = true` solo si:
     - El login está disponible (`login_disponible = true`)
     - El correo existe en clientes (`correo_en_clientes = true`)

#### Respuesta Exitosa (200 OK)

```json
{
  "login_disponible": true,
  "correo_en_clientes": true,
  "cliente": {
    "id_cliente": 123,
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
    "representante": null,
    "id_estatus": 1
  },
  "puede_registrar": true,
  "mensaje": "Login disponible. Se encontró cliente 'Juan Pérez González'"
}
```

#### Casos de Error

**Login no disponible:**
```json
{
  "login_disponible": false,
  "correo_en_clientes": true,
  "cliente": null,
  "puede_registrar": false,
  "mensaje": "El login 'cliente123' ya está en uso"
}
```

**Correo no encontrado en clientes:**
```json
{
  "login_disponible": true,
  "correo_en_clientes": false,
  "cliente": null,
  "puede_registrar": false,
  "mensaje": "No se encontró cliente con el correo 'cliente@email.com'"
}
```

#### Ejemplo cURL

```bash
curl -X POST "https://app-interface-innpulse360-production.up.railway.app/api/v1/usuarios/verificar-disponibilidad" \
  -H "Content-Type: application/json" \
  -d '{
    "login": "cliente123",
    "correo_electronico": "cliente@email.com"
  }'
```

---

### Paso 2: Registrar Usuario-Cliente

#### Endpoint

```
POST /api/v1/usuarios/registro-cliente
```

#### Autenticación

- **Requerida**: No

#### Datos Requeridos

```json
{
  "login": "cliente123",
  "correo_electronico": "cliente@email.com",
  "password": null,
  "cliente_id": 123
}
```

**Campos:**
- `login` (string, requerido): Login del usuario (debe estar disponible)
- `correo_electronico` (string, requerido): Correo electrónico (debe coincidir con el del cliente)
- `password` (string, opcional): Contraseña personalizada
  - Si se proporciona: debe cumplir validación de fortaleza
  - Si es `null`: se genera automáticamente una contraseña temporal
- `cliente_id` (integer, requerido): ID del cliente a asociar

#### Proceso Interno

1. **Validación de login**
   - Verifica que el login no exista
   - Si existe, lanza error: `"El login 'X' ya está en uso"`

2. **Validación de cliente**
   - Verifica que el cliente con `cliente_id` exista
   - Si no existe, lanza error: `"No se encontró cliente con ID X"`

3. **Validación de correo**
   - Verifica que el correo coincida con el del cliente
   - Si no coincide, lanza error: `"El correo no coincide con el del cliente"`

4. **Gestión de contraseña**
   - **Si se proporciona `password`:**
     - Valida fortaleza: mínimo 6 caracteres, al menos una mayúscula, una minúscula y un número
     - Si no cumple, lanza error con el mensaje de validación
     - Usa la contraseña proporcionada
   - **Si `password` es `null`:**
     - Genera una contraseña temporal automática (12 caracteres)
     - Marca `password_temporal = true`
     - Establece `password_expira = fecha_actual + 7 días`

5. **Creación del usuario**
   - Encripta la contraseña con Argon2
   - Crea el usuario en la base de datos
   - Asigna foto de perfil por defecto

6. **Actualización de campos temporales**
   - Si se generó password temporal, actualiza:
     - `password_temporal = true`
     - `password_expira = fecha_expiración`

7. **Asignación de rol**
   - Busca el rol "Cliente" en la base de datos
   - Asigna automáticamente el rol "Cliente" al usuario
   - Si el rol no existe, lanza error: `"No se encontró el rol 'Cliente'"`

8. **Asignación usuario-cliente**
   - Crea la relación entre el usuario y el cliente en la tabla de asignaciones

9. **Envío de email** (si aplica)
   - Si se generó password temporal:
     - Envía email al cliente con:
       - Login
       - Contraseña temporal generada
       - Fecha de expiración
       - Instrucciones para cambiar la contraseña
   - Si falla el envío, no interrumpe el registro (solo se registra en logs)

#### Respuesta Exitosa (201 Created)

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
  "email_enviado": true,
  "mensaje": "Usuario creado exitosamente. Se han enviado las credenciales al correo electrónico proporcionado."
}
```

**⚠️ Nota de Seguridad:** La contraseña temporal **NO se devuelve** en la respuesta. Se envía únicamente por email al cliente.

#### Errores Posibles

- `400 Bad Request`: Login ya en uso
- `400 Bad Request`: Cliente no encontrado
- `400 Bad Request`: El correo no coincide con el del cliente
- `400 Bad Request`: Contraseña no cumple requisitos de fortaleza
- `500 Internal Server Error`: Error al enviar email (no interrumpe el registro)

#### Ejemplo cURL

```bash
curl -X POST "https://app-interface-innpulse360-production.up.railway.app/api/v1/usuarios/registro-cliente" \
  -H "Content-Type: application/json" \
  -d '{
    "login": "cliente123",
    "correo_electronico": "cliente@email.com",
    "password": null,
    "cliente_id": 123
  }'
```

---

### Paso 3: Cambiar Contraseña Temporal (Opcional pero Recomendado)

#### Endpoint

```
POST /api/v1/usuarios/cambiar-password-temporal
```

#### Autenticación

- **Requerida**: No

#### Cuándo Usar

Este endpoint se usa cuando:
- El usuario fue creado con password temporal (generada automáticamente)
- El usuario quiere cambiar su contraseña temporal por una definitiva
- El usuario recibió las credenciales por email y quiere establecer su propia contraseña

#### Datos Requeridos

```json
{
  "login": "cliente123",
  "password_actual": "A1b2C3d4E5f6",
  "password_nueva": "MiNuevaPassword123",
  "password_confirmacion": "MiNuevaPassword123"
}
```

**Campos:**
- `login` (string, requerido): Login del usuario
- `password_actual` (string, requerido): Password temporal actual (recibida por email)
- `password_nueva` (string, requerido): Nueva contraseña (mínimo 6 caracteres)
- `password_confirmacion` (string, requerido): Confirmación de nueva contraseña (debe coincidir)

#### Proceso Interno

1. **Validación de usuario**
   - Busca el usuario por `login`
   - Si no existe, lanza error: `"Usuario no encontrado"`

2. **Validación de contraseña actual**
   - Verifica que `password_actual` sea correcta
   - Si no coincide, lanza error: `"Contraseña actual incorrecta"`

3. **Validación de password temporal**
   - Verifica que el usuario tenga `password_temporal = true`
   - Si no tiene, lanza error: `"Este usuario no tiene una contraseña temporal"`

4. **Validación de expiración**
   - Verifica que `password_expira` no haya pasado
   - Si expiró, lanza error: `"La contraseña temporal ha expirado. Solicite una nueva."`

5. **Validación de nueva contraseña**
   - Valida fortaleza: mínimo 6 caracteres, al menos una mayúscula, una minúscula y un número
   - Si no cumple, lanza error con el mensaje de validación

6. **Validación de confirmación**
   - Verifica que `password_nueva` y `password_confirmacion` coincidan
   - Si no coinciden, lanza error: `"Las contraseñas no coinciden"`

7. **Actualización**
   - Encripta la nueva contraseña con Argon2
   - Actualiza: `password = nueva_contraseña_encriptada`
   - Marca: `password_temporal = false`
   - Limpia: `password_expira = null`
   - Registra: `fecha_ultimo_cambio_password = fecha_actual`

#### Respuesta Exitosa (200 OK)

```json
{
  "success": true,
  "mensaje": "Contraseña actualizada exitosamente. Por favor, inicie sesión con su nueva contraseña.",
  "requiere_login": true
}
```

#### Errores Posibles

- `400 Bad Request`: Usuario no encontrado
- `400 Bad Request`: Contraseña actual incorrecta
- `400 Bad Request`: Este usuario no tiene una contraseña temporal
- `400 Bad Request`: La contraseña temporal ha expirado
- `400 Bad Request`: Contraseña no cumple requisitos de fortaleza
- `400 Bad Request`: Las contraseñas no coinciden

#### Ejemplo cURL

```bash
curl -X POST "https://app-interface-innpulse360-production.up.railway.app/api/v1/usuarios/cambiar-password-temporal" \
  -H "Content-Type: application/json" \
  -d '{
    "login": "cliente123",
    "password_actual": "A1b2C3d4E5f6",
    "password_nueva": "MiNuevaPassword123",
    "password_confirmacion": "MiNuevaPassword123"
  }'
```

---

## Flujo 3: Iniciar Sesión (Acceso a la Plataforma)

### Descripción

Una vez que el usuario existe en el sistema (ya sea creado por administrador o registrado como cliente), puede iniciar sesión para acceder a la plataforma.

### Endpoint

```
POST /api/v1/usuarios/login
```

### Autenticación

- **Requerida**: No

### Datos Requeridos

```json
{
  "login": "cliente123",
  "password": "MiNuevaPassword123"
}
```

**Campos:**
- `login` (string, requerido): Login del usuario
- `password` (string, requerido): Contraseña del usuario

### Proceso Interno

1. **Autenticación**
   - Busca el usuario por `login`
   - Verifica que la contraseña coincida (usando Argon2)
   - Si no coincide, lanza error: `"Credenciales incorrectas"`

2. **Validación de estatus**
   - Verifica que `estatus_id = 1` (activo)
   - Si está inactivo, lanza error: `"Usuario inactivo"`

3. **Validación de password temporal** (si aplica)
   - Si tiene `password_temporal = true`:
     - Verifica que `password_expira` no haya pasado
     - Si expiró, lanza error: `"La contraseña temporal ha expirado. Por favor, contacte al administrador."`
     - Calcula días restantes hasta expiración
     - Prepara información de password temporal para la respuesta

4. **Obtención de módulos**
   - Obtiene todos los módulos a los que el usuario tiene acceso según sus roles
   - Cada módulo incluye: `id_modulo`, `nombre`, `descripcion`, `icono`, `ruta`

5. **Generación de token JWT**
   - Crea un token JWT con:
     - `sub`: ID del usuario
     - `login`: Login del usuario
     - `correo_electronico`: Email del usuario
     - `exp`: Fecha de expiración (30 minutos desde ahora)
   - Algoritmo: HS256
   - Secret Key: Configurada en variables de entorno

6. **Preparación de respuesta**
   - Incluye token, información del usuario, módulos accesibles y estado de password temporal

### Respuesta Exitosa (200 OK)

**Usuario sin password temporal:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0NSIsImxvZ2luIjoiY2xpZW50ZTEyMyIsImNvcnJlb19lbGVjdHJvbmljbyI6ImNsaWVudGVAbWFpbC5jb20iLCJleHAiOjE3MDk4NzYwMDB9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "usuario": {
    "id_usuario": 45,
    "login": "cliente123",
    "correo_electronico": "cliente@email.com"
  },
  "modulos": [
    {
      "id_modulo": 1,
      "nombre": "Dashboard",
      "descripcion": "Panel principal del sistema",
      "icono": "fas fa-dashboard",
      "ruta": "/dashboard"
    },
    {
      "id_modulo": 2,
      "nombre": "Reservaciones",
      "descripcion": "Gestión de reservaciones",
      "icono": "fas fa-calendar",
      "ruta": "/reservaciones"
    }
  ],
  "password_temporal_info": null
}
```

**Usuario con password temporal activa:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "usuario": {
    "id_usuario": 45,
    "login": "cliente123",
    "correo_electronico": "cliente@email.com"
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
  "password_temporal_info": {
    "requiere_cambio": true,
    "password_expira": "2024-12-08T10:00:00",
    "dias_restantes": 5,
    "mensaje": "Debe cambiar su contraseña temporal. Expira en 5 días."
  }
}
```

### Errores Posibles

- `401 Unauthorized`: Credenciales incorrectas
- `401 Unauthorized`: Usuario inactivo
- `401 Unauthorized`: La contraseña temporal ha expirado
- `400 Bad Request`: Datos de entrada inválidos

### Uso del Token

Una vez obtenido el token, debe incluirse en todas las peticiones autenticadas:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Duración del token:** 30 minutos (1800 segundos)

### Ejemplo cURL

```bash
curl -X POST "https://app-interface-innpulse360-production.up.railway.app/api/v1/usuarios/login" \
  -H "Content-Type: application/json" \
  -d '{
    "login": "cliente123",
    "password": "MiNuevaPassword123"
  }'
```

### Ejemplo de Uso del Token

```bash
# Obtener hoteles (requiere autenticación)
curl -X GET "https://app-interface-innpulse360-production.up.railway.app/api/v1/hotel/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## Resumen del Flujo Completo

### Flujo de Registro de Cliente (Autoregistro)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Cliente existe en BD (previamente creado por admin)      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Cliente accede a pantalla de registro                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Ingresa login y correo                                   │
│    → POST /api/v1/usuarios/verificar-disponibilidad        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Validación:                                               │
│    ✓ Login disponible                                       │
│    ✓ Correo existe en clientes                              │
│    → puede_registrar = true                                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Registrar usuario-cliente                                 │
│    → POST /api/v1/usuarios/registro-cliente                 │
│    - password: null (se genera automáticamente)              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Sistema genera password temporal                          │
│    - Expira en 7 días                                       │
│    - Envía email con credenciales                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. Cliente recibe email con:                                 │
│    - Login                                                   │
│    - Password temporal                                      │
│    - Fecha de expiración                                    │
│    - Instrucciones para cambiar contraseña                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 8. (Opcional) Cambiar password temporal                      │
│    → POST /api/v1/usuarios/cambiar-password-temporal       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 9. Iniciar sesión                                            │
│    → POST /api/v1/usuarios/login                            │
│    - Recibe token JWT válido por 30 minutos                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 10. Accede a la plataforma                                   │
│     - Usa token en header Authorization: Bearer <token>      │
│     - Tiene acceso según roles asignados                    │
└─────────────────────────────────────────────────────────────┘
```

### Flujo de Creación por Administrador

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Administrador autenticado                                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Crear usuario                                             │
│    → POST /api/v1/usuarios/                                  │
│    - login, correo, password, roles                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Usuario creado exitosamente                               │
│    - Contraseña encriptada                                  │
│    - Roles asignados                                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Usuario puede iniciar sesión inmediatamente               │
│    → POST /api/v1/usuarios/login                            │
└─────────────────────────────────────────────────────────────┘
```

---

## Estado Actual en la App Móvil

### Situación Actual

**✅ Implementado:**
- Pantalla de login (`LoginScreen`)
- Servicio de autenticación (`AuthService`)
- Controlador de autenticación (`AuthController`)
- Almacenamiento de sesión (`SessionStorage`)
- Integración con endpoint de login

**❌ No Implementado:**
- Pantalla de registro (`RegisterScreen` - solo muestra texto)
- Integración con endpoint de verificación de disponibilidad
- Integración con endpoint de registro de cliente
- Pantalla para cambiar contraseña temporal
- Manejo de password temporal en el login
- Validación de expiración de password temporal

### Archivos Relacionados

**App Móvil:**
- `lib/features/login/register_screen.dart` - Pantalla vacía
- `lib/features/login/login_screen.dart` - Implementado
- `lib/core/auth/services/auth_service.dart` - Solo tiene método `login()`
- `lib/core/auth/controllers/auth_controller.dart` - Solo tiene método `login()`

**API:**
- `api/v1/routes_usuario.py` - Todos los endpoints implementados
- `services/seguridad/usuario_service.py` - Lógica completa implementada
- `schemas/seguridad/registro_cliente_schemas.py` - Schemas definidos

### Lo que Falta Implementar en la App Móvil

1. **Pantalla de Registro Completa**
   - Formulario con campos: login, correo electrónico
   - Botón para verificar disponibilidad
   - Mostrar información del cliente encontrado
   - Botón para registrar
   - Manejo de errores

2. **Servicio de Registro**
   - Método `verificarDisponibilidad()`
   - Método `registrarCliente()`
   - Método `cambiarPasswordTemporal()`

3. **Controlador de Registro**
   - Estados: loading, error, cliente encontrado
   - Métodos para cada operación
   - Manejo de respuestas

4. **Pantalla de Cambio de Contraseña**
   - Formulario con campos: password actual, password nueva, confirmación
   - Validaciones
   - Integración con endpoint

5. **Manejo de Password Temporal en Login**
   - Detectar si tiene password temporal
   - Mostrar alerta o redirigir a pantalla de cambio
   - Validar expiración

---

## Diagramas de Flujo

### Diagrama de Secuencia - Registro de Cliente

```
Cliente          App Móvil          API                    BD              Email Service
  │                  │                │                      │                    │
  │───Registro──────>│                │                      │                    │
  │                  │                │                      │                    │
  │                  │──Verificar────>│                      │                    │
  │                  │  Disponibilidad│                      │                    │
  │                  │                │──Buscar Cliente─────>│                    │
  │                  │                │                      │                    │
  │                  │                │<──Cliente Encontrado─│                    │
  │                  │<──Respuesta────│                      │                    │
  │                  │                │                      │                    │
  │                  │──Registrar────>│                      │                    │
  │                  │  Usuario       │                      │                    │
  │                  │                │──Crear Usuario──────>│                    │
  │                  │                │──Generar Password───>│                    │
  │                  │                │──Asignar Rol────────>│                    │
  │                  │                │──Asignar Cliente───>│                    │
  │                  │                │                      │                    │
  │                  │                │──Enviar Email────────┼───────────────────>│
  │                  │                │                      │                    │
  │                  │                │<──Email Enviado───────┼───────────────────<│
  │                  │<──Confirmación─│                      │                    │
  │                  │                │                      │                    │
  │<──Email──────────┼────────────────┼──────────────────────┼───────────────────<│
  │  (Credenciales)  │                │                      │                    │
  │                  │                │                      │                    │
  │──Cambiar Pass───>│                │                      │                    │
  │                  │──Cambiar──────>│                      │                    │
  │                  │  Password      │──Actualizar─────────>│                    │
  │                  │                │                      │                    │
  │                  │<──Confirmación─│<──Actualizado────────│                    │
  │                  │                │                      │                    │
  │──Login──────────>│                │                      │                    │
  │                  │──Login────────>│                      │                    │
  │                  │                │──Validar────────────>│                    │
  │                  │                │                      │                    │
  │                  │<──Token JWT────│<──Token Generado─────│                    │
  │                  │                │                      │                    │
  │<──Acceso─────────│                │                      │                    │
```

---

## Ejemplos de Código

### Ejemplo: Verificar Disponibilidad (JavaScript)

```javascript
async function verificarDisponibilidad(login, correo) {
  const response = await fetch(
    'https://app-interface-innpulse360-production.up.railway.app/api/v1/usuarios/verificar-disponibilidad',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        login: login,
        correo_electronico: correo
      })
    }
  );
  
  const data = await response.json();
  
  if (data.puede_registrar) {
    console.log('Puede registrar:', data.mensaje);
    console.log('Cliente encontrado:', data.cliente);
  } else {
    console.error('No puede registrar:', data.mensaje);
  }
  
  return data;
}
```

### Ejemplo: Registrar Cliente (JavaScript)

```javascript
async function registrarCliente(login, correo, clienteId) {
  const response = await fetch(
    'https://app-interface-innpulse360-production.up.railway.app/api/v1/usuarios/registro-cliente',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        login: login,
        correo_electronico: correo,
        password: null, // Se genera automáticamente
        cliente_id: clienteId
      })
    }
  );
  
  const data = await response.json();
  
  if (data.usuario_creado) {
    console.log('Usuario creado:', data.mensaje);
    if (data.password_temporal_generada) {
      console.log('Se generó password temporal');
      console.log('Email enviado:', data.email_enviado);
    }
  }
  
  return data;
}
```

### Ejemplo: Cambiar Password Temporal (JavaScript)

```javascript
async function cambiarPasswordTemporal(login, passwordActual, passwordNueva) {
  const response = await fetch(
    'https://app-interface-innpulse360-production.up.railway.app/api/v1/usuarios/cambiar-password-temporal',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        login: login,
        password_actual: passwordActual,
        password_nueva: passwordNueva,
        password_confirmacion: passwordNueva
      })
    }
  );
  
  const data = await response.json();
  
  if (data.success) {
    console.log('Contraseña actualizada:', data.mensaje);
    if (data.requiere_login) {
      // Redirigir a pantalla de login
    }
  }
  
  return data;
}
```

### Ejemplo: Login (JavaScript)

```javascript
async function login(login, password) {
  const response = await fetch(
    'https://app-interface-innpulse360-production.up.railway.app/api/v1/usuarios/login',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        login: login,
        password: password
      })
    }
  );
  
  const data = await response.json();
  
  if (data.access_token) {
    // Guardar token
    localStorage.setItem('token', data.access_token);
    
    // Verificar si tiene password temporal
    if (data.password_temporal_info && data.password_temporal_info.requiere_cambio) {
      console.warn('Debe cambiar su contraseña temporal');
      console.log('Días restantes:', data.password_temporal_info.dias_restantes);
      // Redirigir a pantalla de cambio de contraseña
    }
    
    // Guardar información del usuario
    localStorage.setItem('usuario', JSON.stringify(data.usuario));
    localStorage.setItem('modulos', JSON.stringify(data.modulos));
  }
  
  return data;
}
```

### Ejemplo: Uso del Token (JavaScript)

```javascript
async function obtenerHoteles() {
  const token = localStorage.getItem('token');
  
  const response = await fetch(
    'https://app-interface-innpulse360-production.up.railway.app/api/v1/hotel/',
    {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    }
  );
  
  if (response.status === 401) {
    // Token expirado, redirigir a login
    localStorage.removeItem('token');
    window.location.href = '/login';
    return;
  }
  
  const hoteles = await response.json();
  return hoteles;
}
```

---

## Notas Importantes

### Seguridad

1. **Contraseñas:**
   - Las contraseñas se encriptan con **Argon2** antes de guardarse
   - Las contraseñas temporales **NO se devuelven** en respuestas JSON
   - Las contraseñas temporales se envían **ÚNICAMENTE por email**

2. **Tokens JWT:**
   - Expiran después de **30 minutos**
   - Deben renovarse periódicamente
   - Se incluyen en header `Authorization: Bearer <token>`

3. **Validaciones:**
   - Login único en todo el sistema
   - Email único en todo el sistema
   - Correo debe coincidir con el del cliente en registro

### Requisitos de Contraseña

**Fortaleza mínima:**
- Mínimo 6 caracteres
- Al menos una mayúscula
- Al menos una minúscula
- Al menos un número

**Contraseña temporal:**
- Se genera automáticamente si no se proporciona
- Longitud: 12 caracteres
- Expira en 7 días
- Se envía por email al cliente

### Roles y Permisos

- Al registrar un cliente, se asigna automáticamente el rol **"Cliente"**
- El rol "Cliente" debe existir en la base de datos
- Los módulos accesibles se determinan por los roles del usuario
- Se retornan en la respuesta del login

### Email

- El sistema envía emails con credenciales cuando se genera password temporal
- Si falla el envío, el registro **NO se interrumpe** (solo se registra en logs)
- El email incluye: login, password temporal, fecha de expiración, instrucciones

---

## Base URL

**Producción:**
```
https://app-interface-innpulse360-production.up.railway.app
```

**Desarrollo:**
```
http://localhost:8000
```

**Prefijo de API:**
```
/api/v1
```

---

**Última actualización:** Diciembre 2024  
**Versión del documento:** 1.0.0


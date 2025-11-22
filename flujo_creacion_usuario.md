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

## Guía Práctica: Cómo Consumir las APIs para Crear Usuarios

Esta sección explica paso a paso cómo consumir las APIs disponibles para crear usuarios y acceder a la plataforma. Incluye ejemplos prácticos de implementación.

### Configuración Inicial

**Base URL de Producción:**
```
https://app-interface-innpulse360-production.up.railway.app
```

**Base URL de Desarrollo:**
```
http://localhost:8000
```

**Prefijo de API:**
```
/api/v1
```

**Headers Comunes:**
```json
{
  "Content-Type": "application/json"
}
```

**Headers con Autenticación:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_TOKEN_HERE"
}
```

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

### Proceso Completo: Cómo Consumir la API

#### Paso 1: Autenticarse como Administrador

Primero, el administrador debe obtener un token de autenticación:

**Request:**
```http
POST /api/v1/usuarios/login
Content-Type: application/json

{
  "login": "admin",
  "password": "AdminPassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "usuario": {
    "id_usuario": 1,
    "login": "admin",
    "correo_electronico": "admin@innpulse360.com"
  },
  "modulos": [...]
}
```

**Guardar el token:** Almacena el `access_token` para usarlo en las siguientes peticiones.

#### Paso 2: Crear el Nuevo Usuario

Con el token obtenido, crear el nuevo usuario:

**Request:**
```http
POST /api/v1/usuarios/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "login": "nuevo.usuario",
  "correo_electronico": "usuario@email.com",
  "password": "Password123",
  "estatus_id": 1,
  "roles_ids": [1, 2]
}
```

**Response (201 Created):**
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

#### Paso 3: Verificar que el Usuario Puede Iniciar Sesión

El usuario creado puede iniciar sesión inmediatamente:

**Request:**
```http
POST /api/v1/usuarios/login
Content-Type: application/json

{
  "login": "nuevo.usuario",
  "password": "Password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "usuario": {
    "id_usuario": 5,
    "login": "nuevo.usuario",
    "correo_electronico": "usuario@email.com"
  },
  "modulos": [...]
}
```

#### Manejo de Errores

**Error 400 - Login o Email ya existe:**
```json
{
  "detail": "El login ya está en uso"
}
```

**Error 401 - Token inválido o expirado:**
```json
{
  "detail": "Token inválido o expirado"
}
```

**Solución:** Renovar el token haciendo login nuevamente.

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

### Proceso Completo: Cómo Consumir las APIs para Registro de Cliente

Este flujo permite que un cliente existente se registre como usuario del sistema. **No requiere autenticación previa**, pero el cliente debe existir en la base de datos.

#### Paso 1: Verificar Disponibilidad

Antes de registrar, verificar que el login esté disponible y que el correo exista en la tabla de clientes:

**Request:**
```http
POST /api/v1/usuarios/verificar-disponibilidad
Content-Type: application/json

{
  "login": "cliente123",
  "correo_electronico": "cliente@email.com"
}
```

**Response Exitosa (200 OK):**
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

**Importante:** 
- Si `puede_registrar` es `true`, puedes proceder al registro
- Guarda el `id_cliente` de la respuesta para usarlo en el siguiente paso
- Si `puede_registrar` es `false`, revisa el `mensaje` para entender el problema

**Casos de Error:**

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

#### Paso 2: Registrar Usuario-Cliente

Una vez verificada la disponibilidad, proceder con el registro:

**Request:**
```http
POST /api/v1/usuarios/registro-cliente
Content-Type: application/json

{
  "login": "cliente123",
  "correo_electronico": "cliente@email.com",
  "password": null,
  "cliente_id": 123
}
```

**Notas importantes:**
- `password`: Puede ser `null` (se genera automáticamente) o una contraseña personalizada
- Si envías `password: null`, el sistema generará una contraseña temporal de 12 caracteres
- La contraseña temporal expira en 7 días
- Si proporcionas una contraseña, debe cumplir los requisitos de fortaleza

**Response Exitosa (201 Created):**
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

**⚠️ Seguridad:** La contraseña temporal **NO se devuelve** en la respuesta JSON. Se envía únicamente por email al cliente.

**Errores Posibles:**

**400 Bad Request - Login ya en uso:**
```json
{
  "detail": "El login 'cliente123' ya está en uso"
}
```

**400 Bad Request - Cliente no encontrado:**
```json
{
  "detail": "No se encontró cliente con ID 123"
}
```

**400 Bad Request - Correo no coincide:**
```json
{
  "detail": "El correo no coincide con el del cliente"
}
```

**400 Bad Request - Contraseña débil:**
```json
{
  "detail": "La contraseña debe tener al menos 6 caracteres, una mayúscula, una minúscula y un número"
}
```

#### Paso 3: Cliente Recibe Email con Credenciales

Si se generó una contraseña temporal, el cliente recibirá un email con:
- Login del usuario
- Contraseña temporal generada
- Fecha de expiración (7 días)
- Instrucciones para cambiar la contraseña

**Nota:** Si el envío de email falla, el registro **NO se interrumpe**. El usuario se crea exitosamente, pero el email no se envía (se registra en logs).

#### Paso 4: (Opcional) Cambiar Contraseña Temporal

El cliente puede cambiar su contraseña temporal por una definitiva:

**Request:**
```http
POST /api/v1/usuarios/cambiar-password-temporal
Content-Type: application/json

{
  "login": "cliente123",
  "password_actual": "A1b2C3d4E5f6",
  "password_nueva": "MiNuevaPassword123",
  "password_confirmacion": "MiNuevaPassword123"
}
```

**Response Exitosa (200 OK):**
```json
{
  "success": true,
  "mensaje": "Contraseña actualizada exitosamente. Por favor, inicie sesión con su nueva contraseña.",
  "requiere_login": true
}
```

**Errores Posibles:**

**400 Bad Request - Contraseña actual incorrecta:**
```json
{
  "detail": "Contraseña actual incorrecta"
}
```

**400 Bad Request - Contraseña temporal expirada:**
```json
{
  "detail": "La contraseña temporal ha expirado. Solicite una nueva."
}
```

**400 Bad Request - Contraseñas no coinciden:**
```json
{
  "detail": "Las contraseñas no coinciden"
}
```

#### Paso 5: Iniciar Sesión

Una vez que el cliente tiene sus credenciales (ya sea la temporal o la definitiva), puede iniciar sesión:

**Request:**
```http
POST /api/v1/usuarios/login
Content-Type: application/json

{
  "login": "cliente123",
  "password": "MiNuevaPassword123"
}
```

**Response Exitosa (200 OK):**
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
      "descripcion": "Panel principal del sistema",
      "icono": "fas fa-dashboard",
      "ruta": "/dashboard"
    }
  ],
  "password_temporal_info": null
}
```

**Si el usuario aún tiene contraseña temporal activa:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "usuario": {...},
  "modulos": [...],
  "password_temporal_info": {
    "requiere_cambio": true,
    "password_expira": "2024-12-08T10:00:00",
    "dias_restantes": 5,
    "mensaje": "Debe cambiar su contraseña temporal. Expira en 5 días."
  }
}
```

**Recomendación:** Si `password_temporal_info.requiere_cambio` es `true`, mostrar una alerta al usuario y redirigirlo a la pantalla de cambio de contraseña.

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

### Proceso Completo: Cómo Consumir la API de Login

#### Paso 1: Realizar Login

**Request:**
```http
POST /api/v1/usuarios/login
Content-Type: application/json

{
  "login": "cliente123",
  "password": "MiNuevaPassword123"
}
```

**Response Exitosa (200 OK):**
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

#### Paso 2: Guardar el Token y la Información del Usuario

**Almacenar en el cliente:**
- `access_token`: Token JWT para autenticación (válido por 30 minutos)
- `usuario`: Información del usuario autenticado
- `modulos`: Lista de módulos a los que tiene acceso según sus roles

**Ejemplo de almacenamiento:**
```javascript
// JavaScript/TypeScript
localStorage.setItem('token', response.access_token);
localStorage.setItem('usuario', JSON.stringify(response.usuario));
localStorage.setItem('modulos', JSON.stringify(response.modulos));
```

#### Paso 3: Usar el Token en Peticiones Autenticadas

Todas las peticiones a endpoints protegidos deben incluir el token en el header `Authorization`:

**Ejemplo - Obtener Hoteles:**
```http
GET /api/v1/hotel/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**Ejemplo - Obtener Perfil del Usuario:**
```http
GET /api/v1/usuarios/me/profile
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

#### Paso 4: Manejar Expiración del Token

El token expira después de 30 minutos (1800 segundos). Cuando recibas un error 401, debes:

1. Limpiar el token almacenado
2. Redirigir al usuario a la pantalla de login
3. Solicitar nuevas credenciales

**Ejemplo de manejo de error:**
```javascript
if (response.status === 401) {
  localStorage.removeItem('token');
  localStorage.removeItem('usuario');
  localStorage.removeItem('modulos');
  window.location.href = '/login';
}
```

#### Manejo de Errores

**401 Unauthorized - Credenciales incorrectas:**
```json
{
  "detail": "Credenciales incorrectas"
}
```

**401 Unauthorized - Usuario inactivo:**
```json
{
  "detail": "Usuario inactivo"
}
```

**401 Unauthorized - Contraseña temporal expirada:**
```json
{
  "detail": "La contraseña temporal ha expirado. Por favor, contacte al administrador."
}
```

**400 Bad Request - Datos inválidos:**
```json
{
  "detail": [
    {
      "loc": ["body", "login"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
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

## Ejemplos de Código Prácticos

Esta sección incluye ejemplos completos de implementación en diferentes lenguajes y frameworks para consumir las APIs de creación de usuario y autenticación.

### JavaScript/TypeScript (Fetch API)

#### Clase de Servicio para Autenticación y Registro

```javascript
class AuthService {
  constructor(baseURL = 'https://app-interface-innpulse360-production.up.railway.app') {
    this.baseURL = baseURL;
    this.apiPrefix = '/api/v1';
  }

  /**
   * Iniciar sesión
   */
  async login(login, password) {
    const response = await fetch(`${this.baseURL}${this.apiPrefix}/usuarios/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ login, password })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Error al iniciar sesión');
    }

    const data = await response.json();
    
    // Guardar token y datos del usuario
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('usuario', JSON.stringify(data.usuario));
    localStorage.setItem('modulos', JSON.stringify(data.modulos));
    
    return data;
  }

  /**
   * Verificar disponibilidad para registro de cliente
   */
  async verificarDisponibilidad(login, correoElectronico) {
    const response = await fetch(`${this.baseURL}${this.apiPrefix}/usuarios/verificar-disponibilidad`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        login,
        correo_electronico: correoElectronico
      })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Error al verificar disponibilidad');
    }

    return await response.json();
  }

  /**
   * Registrar usuario-cliente
   */
  async registrarCliente(login, correoElectronico, clienteId, password = null) {
    const response = await fetch(`${this.baseURL}${this.apiPrefix}/usuarios/registro-cliente`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        login,
        correo_electronico: correoElectronico,
        password,
        cliente_id: clienteId
      })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Error al registrar cliente');
    }

    return await response.json();
  }

  /**
   * Cambiar contraseña temporal
   */
  async cambiarPasswordTemporal(login, passwordActual, passwordNueva, passwordConfirmacion) {
    const response = await fetch(`${this.baseURL}${this.apiPrefix}/usuarios/cambiar-password-temporal`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        login,
        password_actual: passwordActual,
        password_nueva: passwordNueva,
        password_confirmacion: passwordConfirmacion
      })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Error al cambiar contraseña');
    }

    return await response.json();
  }

  /**
   * Crear usuario (requiere autenticación de administrador)
   */
  async crearUsuario(usuarioData) {
    const token = localStorage.getItem('token');
    
    if (!token) {
      throw new Error('No hay token de autenticación');
    }

    const response = await fetch(`${this.baseURL}${this.apiPrefix}/usuarios/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(usuarioData)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Error al crear usuario');
    }

    return await response.json();
  }

  /**
   * Obtener token almacenado
   */
  getToken() {
    return localStorage.getItem('token');
  }

  /**
   * Verificar si hay sesión activa
   */
  isAuthenticated() {
    return !!this.getToken();
  }

  /**
   * Cerrar sesión
   */
  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('usuario');
    localStorage.removeItem('modulos');
  }
}

// Uso del servicio
const authService = new AuthService();

// Ejemplo: Flujo completo de registro de cliente
async function flujoRegistroCliente() {
  try {
    // 1. Verificar disponibilidad
    const verificacion = await authService.verificarDisponibilidad(
      'cliente123',
      'cliente@email.com'
    );

    if (!verificacion.puede_registrar) {
      console.error('No se puede registrar:', verificacion.mensaje);
      return;
    }

    console.log('Cliente encontrado:', verificacion.cliente);

    // 2. Registrar usuario-cliente
    const registro = await authService.registrarCliente(
      'cliente123',
      'cliente@email.com',
      verificacion.cliente.id_cliente,
      null // Se genera contraseña temporal automáticamente
    );

    console.log('Usuario creado:', registro.mensaje);
    console.log('Email enviado:', registro.email_enviado);

    // 3. El cliente recibirá las credenciales por email
    // 4. Cuando tenga las credenciales, puede iniciar sesión
    const login = await authService.login('cliente123', 'PasswordTemporal123');
    console.log('Login exitoso:', login.usuario);

  } catch (error) {
    console.error('Error en el flujo:', error.message);
  }
}
```

### Python (Requests)

```python
import requests
from typing import Optional, Dict, Any

class AuthService:
    def __init__(self, base_url: str = "https://app-interface-innpulse360-production.up.railway.app"):
        self.base_url = base_url
        self.api_prefix = "/api/v1"
        self.token: Optional[str] = None

    def login(self, login: str, password: str) -> Dict[str, Any]:
        """Iniciar sesión"""
        url = f"{self.base_url}{self.api_prefix}/usuarios/login"
        response = requests.post(
            url,
            json={"login": login, "password": password},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        
        data = response.json()
        self.token = data["access_token"]
        return data

    def verificar_disponibilidad(self, login: str, correo_electronico: str) -> Dict[str, Any]:
        """Verificar disponibilidad para registro de cliente"""
        url = f"{self.base_url}{self.api_prefix}/usuarios/verificar-disponibilidad"
        response = requests.post(
            url,
            json={
                "login": login,
                "correo_electronico": correo_electronico
            },
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()

    def registrar_cliente(
        self,
        login: str,
        correo_electronico: str,
        cliente_id: int,
        password: Optional[str] = None
    ) -> Dict[str, Any]:
        """Registrar usuario-cliente"""
        url = f"{self.base_url}{self.api_prefix}/usuarios/registro-cliente"
        response = requests.post(
            url,
            json={
                "login": login,
                "correo_electronico": correo_electronico,
                "password": password,
                "cliente_id": cliente_id
            },
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()

    def cambiar_password_temporal(
        self,
        login: str,
        password_actual: str,
        password_nueva: str,
        password_confirmacion: str
    ) -> Dict[str, Any]:
        """Cambiar contraseña temporal"""
        url = f"{self.base_url}{self.api_prefix}/usuarios/cambiar-password-temporal"
        response = requests.post(
            url,
            json={
                "login": login,
                "password_actual": password_actual,
                "password_nueva": password_nueva,
                "password_confirmacion": password_confirmacion
            },
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()

    def crear_usuario(self, usuario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear usuario (requiere autenticación de administrador)"""
        if not self.token:
            raise ValueError("No hay token de autenticación")

        url = f"{self.base_url}{self.api_prefix}/usuarios/"
        response = requests.post(
            url,
            json=usuario_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}"
            }
        )
        response.raise_for_status()
        return response.json()

# Uso del servicio
auth_service = AuthService()

# Ejemplo: Flujo completo de registro de cliente
def flujo_registro_cliente():
    try:
        # 1. Verificar disponibilidad
        verificacion = auth_service.verificar_disponibilidad(
            "cliente123",
            "cliente@email.com"
        )

        if not verificacion["puede_registrar"]:
            print(f"No se puede registrar: {verificacion['mensaje']}")
            return

        print(f"Cliente encontrado: {verificacion['cliente']['nombre_razon_social']}")

        # 2. Registrar usuario-cliente
        registro = auth_service.registrar_cliente(
            "cliente123",
            "cliente@email.com",
            verificacion["cliente"]["id_cliente"],
            None  # Se genera contraseña temporal automáticamente
        )

        print(f"Usuario creado: {registro['mensaje']}")
        print(f"Email enviado: {registro['email_enviado']}")

        # 3. El cliente recibirá las credenciales por email
        # 4. Cuando tenga las credenciales, puede iniciar sesión
        login = auth_service.login("cliente123", "PasswordTemporal123")
        print(f"Login exitoso: {login['usuario']['login']}")

    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP: {e}")
    except Exception as e:
        print(f"Error en el flujo: {e}")
```

### Dart/Flutter

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class AuthService {
  final String baseURL;
  String? token;

  AuthService({
    this.baseURL = 'https://app-interface-innpulse360-production.up.railway.app',
  });

  final String apiPrefix = '/api/v1';

  /// Iniciar sesión
  Future<Map<String, dynamic>> login(String login, String password) async {
    final url = Uri.parse('$baseURL$apiPrefix/usuarios/login');
    
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'login': login,
        'password': password,
      }),
    );

    if (response.statusCode != 200) {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Error al iniciar sesión');
    }

    final data = jsonDecode(response.body);
    token = data['access_token'];
    return data;
  }

  /// Verificar disponibilidad para registro de cliente
  Future<Map<String, dynamic>> verificarDisponibilidad(
    String login,
    String correoElectronico,
  ) async {
    final url = Uri.parse('$baseURL$apiPrefix/usuarios/verificar-disponibilidad');
    
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'login': login,
        'correo_electronico': correoElectronico,
      }),
    );

    if (response.statusCode != 200) {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Error al verificar disponibilidad');
    }

    return jsonDecode(response.body);
  }

  /// Registrar usuario-cliente
  Future<Map<String, dynamic>> registrarCliente({
    required String login,
    required String correoElectronico,
    required int clienteId,
    String? password,
  }) async {
    final url = Uri.parse('$baseURL$apiPrefix/usuarios/registro-cliente');
    
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'login': login,
        'correo_electronico': correoElectronico,
        'password': password,
        'cliente_id': clienteId,
      }),
    );

    if (response.statusCode != 201) {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Error al registrar cliente');
    }

    return jsonDecode(response.body);
  }

  /// Cambiar contraseña temporal
  Future<Map<String, dynamic>> cambiarPasswordTemporal({
    required String login,
    required String passwordActual,
    required String passwordNueva,
    required String passwordConfirmacion,
  }) async {
    final url = Uri.parse('$baseURL$apiPrefix/usuarios/cambiar-password-temporal');
    
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'login': login,
        'password_actual': passwordActual,
        'password_nueva': passwordNueva,
        'password_confirmacion': passwordConfirmacion,
      }),
    );

    if (response.statusCode != 200) {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Error al cambiar contraseña');
    }

    return jsonDecode(response.body);
  }

  /// Crear usuario (requiere autenticación de administrador)
  Future<Map<String, dynamic>> crearUsuario(Map<String, dynamic> usuarioData) async {
    if (token == null) {
      throw Exception('No hay token de autenticación');
    }

    final url = Uri.parse('$baseURL$apiPrefix/usuarios/');
    
    final response = await http.post(
      url,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode(usuarioData),
    );

    if (response.statusCode != 201) {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Error al crear usuario');
    }

    return jsonDecode(response.body);
  }
}

// Uso del servicio
void ejemploFlujoRegistroCliente() async {
  final authService = AuthService();

  try {
    // 1. Verificar disponibilidad
    final verificacion = await authService.verificarDisponibilidad(
      'cliente123',
      'cliente@email.com',
    );

    if (!verificacion['puede_registrar']) {
      print('No se puede registrar: ${verificacion['mensaje']}');
      return;
    }

    print('Cliente encontrado: ${verificacion['cliente']['nombre_razon_social']}');

    // 2. Registrar usuario-cliente
    final registro = await authService.registrarCliente(
      login: 'cliente123',
      correoElectronico: 'cliente@email.com',
      clienteId: verificacion['cliente']['id_cliente'],
      password: null, // Se genera contraseña temporal automáticamente
    );

    print('Usuario creado: ${registro['mensaje']}');
    print('Email enviado: ${registro['email_enviado']}');

    // 3. El cliente recibirá las credenciales por email
    // 4. Cuando tenga las credenciales, puede iniciar sesión
    final login = await authService.login('cliente123', 'PasswordTemporal123');
    print('Login exitoso: ${login['usuario']['login']}');

  } catch (e) {
    print('Error en el flujo: $e');
  }
}
```

### Ejemplos de Código Originales

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

---

## Resumen Ejecutivo: Pasos para Consumir las APIs

### Flujo 1: Crear Usuario como Administrador

1. **Autenticarse como administrador**
   - `POST /api/v1/usuarios/login`
   - Guardar el `access_token` recibido

2. **Crear nuevo usuario**
   - `POST /api/v1/usuarios/`
   - Incluir header: `Authorization: Bearer {token}`
   - Enviar: `login`, `correo_electronico`, `password`, `estatus_id`, `roles_ids`

3. **Usuario puede iniciar sesión inmediatamente**
   - `POST /api/v1/usuarios/login`
   - Usar las credenciales proporcionadas

### Flujo 2: Registro de Cliente (Autoregistro)

1. **Verificar disponibilidad**
   - `POST /api/v1/usuarios/verificar-disponibilidad`
   - Enviar: `login`, `correo_electronico`
   - Verificar que `puede_registrar` sea `true`
   - Guardar `cliente.id_cliente`

2. **Registrar usuario-cliente**
   - `POST /api/v1/usuarios/registro-cliente`
   - Enviar: `login`, `correo_electronico`, `cliente_id`, `password` (opcional)
   - Si `password` es `null`, se genera automáticamente y se envía por email

3. **Cliente recibe credenciales por email**
   - Login y contraseña temporal (si se generó automáticamente)
   - Fecha de expiración (7 días)

4. **Cambiar contraseña temporal (opcional pero recomendado)**
   - `POST /api/v1/usuarios/cambiar-password-temporal`
   - Enviar: `login`, `password_actual`, `password_nueva`, `password_confirmacion`

5. **Iniciar sesión**
   - `POST /api/v1/usuarios/login`
   - Usar credenciales (temporal o definitiva)

### Flujo 3: Iniciar Sesión

1. **Autenticarse**
   - `POST /api/v1/usuarios/login`
   - Enviar: `login`, `password`

2. **Guardar token y datos**
   - Almacenar `access_token` (válido 30 minutos)
   - Guardar `usuario` y `modulos` para uso en la aplicación

3. **Usar token en peticiones autenticadas**
   - Incluir header: `Authorization: Bearer {token}`
   - Renovar token cuando expire (hacer login nuevamente)

### Checklist de Implementación

- [ ] Configurar base URL (producción o desarrollo)
- [ ] Implementar servicio de autenticación
- [ ] Manejar almacenamiento de token (localStorage, SharedPreferences, etc.)
- [ ] Implementar interceptor para agregar token a peticiones autenticadas
- [ ] Manejar expiración de token (error 401)
- [ ] Implementar pantalla de login
- [ ] Implementar pantalla de registro de cliente
- [ ] Implementar pantalla de cambio de contraseña temporal
- [ ] Manejar errores de API (400, 401, 404, 500)
- [ ] Mostrar mensajes de éxito/error al usuario
- [ ] Validar datos antes de enviar (formato de email, fortaleza de contraseña, etc.)

### Consideraciones de Seguridad

1. **Nunca almacenes contraseñas en texto plano**
   - Las contraseñas se encriptan automáticamente en el servidor
   - Las contraseñas temporales solo se envían por email

2. **Maneja los tokens de forma segura**
   - Almacena el token en un lugar seguro (no en cookies públicas)
   - No expongas el token en URLs o logs
   - Renueva el token antes de que expire

3. **Valida datos en el cliente**
   - Verifica formato de email
   - Valida fortaleza de contraseña antes de enviar
   - Verifica que los campos requeridos estén presentes

4. **Maneja errores apropiadamente**
   - No muestres mensajes de error técnicos al usuario final
   - Proporciona mensajes claros y accionables
   - Registra errores para debugging

---

**Última actualización:** Diciembre 2024  
**Versión del documento:** 2.0.0


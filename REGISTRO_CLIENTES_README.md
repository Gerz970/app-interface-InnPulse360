
### **2. Registro de Usuario-Cliente**
```
POST /api/v1/usuarios/registro-cliente
```

**Request:**
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

### **3. Cambiar Password Temporal**
```
POST /api/v1/usuarios/cambiar-password-temporal
```

**Request:**
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
  "mensaje": "Contraseña actualizada exitosamente. Por favor, inicie sesión con su nueva contraseña.",
  "requiere_login": true
}
```

---

### **4. Login con Validación de Password Temporal**
```
POST /api/v1/usuarios/login
```

**Request:**
```json
{
  "login": "cliente123",
  "password": "A1b2C3d4E5f6"
}
```

**Response (si tiene password temporal):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user_info": {
    "id_usuario": 45,
    "login": "cliente123",
    "correo_electronico": "cliente@email.com",
    "password_temporal": {
      "requiere_cambio": true,
      "password_expira": "2024-01-22T10:30:00",
      "dias_restantes": 5,
      "mensaje": "Debe cambiar su contraseña temporal. Expira en 5 días."
    }
  }
}
```

---

## 🔄 Flujo Completo de Registro

### **Paso 1: Frontend - Verificación**
```javascript
const verificacion = await fetch('/api/v1/usuarios/verificar-disponibilidad', {
  method: 'POST',
  body: JSON.stringify({
    login: 'cliente123',
    correo_electronico: 'cliente@email.com'
  })
});

const result = await verificacion.json();

if (!result.puede_registrar) {
  console.error(result.mensaje);
  return;
}
```

### **Paso 2: Frontend - Registro**
```javascript
const registro = await fetch('/api/v1/usuarios/registro-cliente', {
  method: 'POST',
  body: JSON.stringify({
    login: 'cliente123',
    correo_electronico: 'cliente@email.com',
    password: null, // Se generará temporal
    cliente_id: result.cliente_encontrado.id_cliente
  })
});

const usuario = await registro.json();

if (usuario.password_temporal_generada) {
  // Mostrar password temporal al usuario
  alert(`Su contraseña temporal es: ${usuario.password_temporal}`);
  alert(`Expira en 7 días`);
}
```

### **Paso 3: Frontend - Primer Login**
```javascript
const login = await fetch('/api/v1/usuarios/login', {
  method: 'POST',
  body: JSON.stringify({
    login: 'cliente123',
    password: 'A1b2C3d4E5f6'
  })
});

const tokenData = await login.json();

if (tokenData.user_info.password_temporal) {
  // Redirigir a pantalla de cambio de contraseña
  window.location.href = '/cambiar-password';
}
```

### **Paso 4: Frontend - Cambio de Password**
```javascript
const cambio = await fetch('/api/v1/usuarios/cambiar-password-temporal', {
  method: 'POST',
  body: JSON.stringify({
    login: 'cliente123',
    password_actual: 'A1b2C3d4E5f6',
    password_nueva: 'MiNuevaPassword123',
    password_confirmacion: 'MiNuevaPassword123'
  })
});

// Redirigir al login
window.location.href = '/login';
```

---

## ⚙️ Validaciones Implementadas

### **Registro:**
- ✅ Login único (no puede existir)
- ✅ Cliente debe existir en BD
- ✅ Correo debe coincidir con el del cliente
- ✅ Password temporal generada automáticamente si no se envía
- ✅ Expiración de 7 días para password temporal

### **Login:**
- ✅ Credenciales válidas
- ✅ Usuario activo
- ✅ **Password temporal no expirada**
- ✅ **Alerta si tiene password temporal activa**

### **Cambio de Password:**
- ✅ Password actual correcta
- ✅ Tiene password temporal activa
- ✅ No ha expirado
- ✅ Nueva password cumple requisitos:
  - Mínimo 6 caracteres
  - Al menos una mayúscula
  - Al menos una minúscula
  - Al menos un número
- ✅ Passwords coinciden

---

## 🔐 Seguridad

### **Password Temporal:**
- Generada con `secrets` (criptográficamente segura)
- Longitud de 12 caracteres
- Incluye mayúsculas, minúsculas y números
- Expira en 7 días
- Se marca en BD (`password_temporal = 1`)

### **Encriptación:**
- Argon2 para hash de contraseñas
- Sin límite de longitud
- Resistente a ataques de fuerza bruta

---

## 📊 Estructura de Tablas

### **SEGURIDAD.Tb_usuario**
```sql
- password_temporal (BIT)
- password_expira (DATETIME)
- fecha_ultimo_cambio_password (DATETIME)
- intentos_login_fallidos (INT)
```

### **SEGURIDAD.Tb_usuarioAsignacion**
```sql
- id_asignacion (INT PK)
- usuario_id (INT FK UNIQUE)
- empleado_id (INT NULL)
- cliente_id (INT FK NULL)
- tipo_asignacion (TINYINT) -- 1=Empleado, 2=Cliente
- fecha_asignacion (DATETIME)
- estatus (TINYINT)
```

---

## ✨ Características Adicionales

- ✅ Relación 1:1 entre usuario y cliente
- ✅ Rol "Cliente" asignado automáticamente
- ✅ Trazabilidad de asignaciones
- ✅ Soporte futuro para empleados (mismo flujo)
- ✅ Validación de fortaleza de contraseñas
- ✅ TODO preparado para integración con EmailService

---

## 🎯 Próximos Pasos (Opcionales)

1. **Integración con EmailService** para enviar credenciales
2. **Reset de password** si expira la temporal
3. **Historial de passwords** para prevenir reutilización
4. **Bloqueo por intentos fallidos** de login
5. **Notificaciones** antes de expiración de password temporal

---

## 📝 Notas Importantes

- El rol "Cliente" **DEBE existir** en la BD antes de usar el sistema
- Las passwords temporales expiran en **7 días**
- El correo del usuario **debe coincidir** con el del cliente
- La validación de password temporal se hace automáticamente en el login
- El frontend debe manejar la redirección al cambio de password

---

Implementado por: AI Assistant  
Fecha: 2024-01-15  
Versión: 1.0.0

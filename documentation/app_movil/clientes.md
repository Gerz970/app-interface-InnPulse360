# Gestión de Clientes

El módulo de clientes permite a los administradores gestionar la información de los clientes del hotel. Este módulo está disponible solo para usuarios con permisos de administración.

## Ver Lista de Clientes

1. Ve a **"Clientes"** en el menú lateral
2. Verás un listado de todos los clientes registrados
3. Cada cliente muestra:
   - Nombre o razón social
   - RFC
   - Correo electrónico
   - Teléfono
   - Estado (Activo/Inactivo)

## Crear un Nuevo Cliente

1. En el listado de clientes, presiona el botón **"+"** o **"Agregar Cliente"**
2. Selecciona el tipo de persona:
   - **Persona Física**: Para clientes individuales
   - **Persona Moral**: Para empresas u organizaciones
3. Completa el formulario según el tipo seleccionado:

### Persona Física
- Nombre
- Apellido Paterno
- Apellido Materno
- RFC (requerido, único)
- CURP
- Correo electrónico
- Teléfono
- Dirección
- País y Estado

### Persona Moral
- Razón Social
- RFC (requerido, único)
- Representante Legal
- Correo electrónico
- Teléfono
- Dirección
- País y Estado

4. Presiona **"Guardar"** para crear el cliente

## Ver Detalle de Cliente

1. Toca cualquier cliente en el listado
2. Verás toda la información del cliente:
   - Datos personales o de la empresa
   - Información de contacto
   - Dirección completa
   - Estado actual

## Editar Cliente

1. Abre el detalle del cliente
2. Presiona **"Editar"**
3. Puedes modificar:
   - Nombre o razón social
   - Teléfono
   - Dirección
   - Estado (Activo/Inactivo)
4. **Nota**: RFC, CURP y apellidos no se pueden editar por restricciones del sistema

## Eliminar Cliente

1. En el detalle del cliente, presiona **"Eliminar"**
2. Confirma la eliminación
3. El cliente será marcado como inactivo (eliminación lógica)

## Búsqueda y Filtros

- Usa la barra de búsqueda para encontrar clientes por nombre o RFC
- El listado muestra hasta 100 clientes por página

## Problemas Comunes

- **Error: RFC duplicado**: El RFC ya está registrado en el sistema. Verifica que no exista otro cliente con el mismo RFC
- **No puedo editar ciertos campos**: Algunos campos como RFC y CURP no son editables por políticas de seguridad
- **Cliente no se puede eliminar**: Si el cliente tiene reservaciones activas o dependencias, no podrá ser eliminado


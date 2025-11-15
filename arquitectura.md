# Arquitectura del Sistema InnPulse360

## 1. Visión General

InnPulse360 es una API REST moderna construida con **FastAPI** para la gestión integral de hoteles. El sistema está diseñado siguiendo principios de **arquitectura limpia** y **separación de responsabilidades**, implementando un patrón de capas bien definido que facilita el mantenimiento, escalabilidad y testabilidad.

## 2. Arquitectura de Capas

El proyecto implementa una arquitectura en capas con las siguientes responsabilidades:

```
┌─────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                  │
│                  (API Routes - FastAPI)                  │
│  api/v1/routes_*.py                                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   CAPA DE SERVICIOS                      │
│              (Lógica de Negocio)                          │
│  services/*/service.py                                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                    CAPA DE ACCESO A DATOS                │
│              (Data Access Objects - DAO)                 │
│  dao/*/dao_*.py                                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                    CAPA DE MODELOS                       │
│              (SQLAlchemy ORM Models)                     │
│  models/*/model.py                                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  BASE DE DATOS                            │
│              SQL Server (MSSQL)                          │
└─────────────────────────────────────────────────────────┘
```

### 2.1. Flujo de Datos

```
Request HTTP
    │
    ▼
[API Routes] → Validación con Pydantic Schemas
    │
    ▼
[Services] → Lógica de negocio, validaciones, transformaciones
    │
    ▼
[DAOs] → Operaciones CRUD en base de datos
    │
    ▼
[Models] → Mapeo ORM SQLAlchemy
    │
    ▼
[SQL Server Database]
    │
    ▼
[Models] → Conversión a Pydantic Schemas
    │
    ▼
[Services] → Transformaciones adicionales
    │
    ▼
[API Routes] → Serialización JSON
    │
    ▼
Response HTTP
```

## 3. Estructura del Proyecto

```
app-interface-InnPulse360/
│
├── main.py                          # Punto de entrada de la aplicación
│
├── api/                             # Capa de Presentación
│   └── v1/                          # Versionado de API
│       ├── __init__.py              # Router principal que agrupa todas las rutas
│       ├── routes_hotel.py          # Endpoints de hoteles
│       ├── routes_usuario.py        # Endpoints de usuarios y autenticación
│       ├── routes_reservacion.py    # Endpoints de reservaciones
│       ├── routes_*.py              # Otros endpoints por módulo
│       └── ...
│
├── core/                            # Configuración y Servicios Core
│   ├── config.py                    # Configuración de la aplicación (Settings)
│   ├── database_connection.py       # Conexión a BD (Patrón Singleton)
│   ├── supabase_client.py           # Cliente Supabase (Patrón Singleton)
│   ├── email_config.py              # Configuración de email
│   ├── base.py                      # Base declarativa SQLAlchemy
│   └── email_templates/             # Plantillas HTML para emails
│       └── base_template.html
│
├── models/                          # Capa de Modelos (SQLAlchemy ORM)
│   ├── hotel/                       # Modelos relacionados con hoteles
│   ├── seguridad/                   # Modelos de usuarios, roles, permisos
│   ├── reserva/                     # Modelos de reservaciones
│   ├── cliente/                     # Modelos de clientes
│   ├── empleado/                    # Modelos de empleados
│   ├── camarista/                   # Modelos de limpieza
│   ├── mantenimiento/               # Modelos de mantenimiento
│   └── catalogos/                   # Modelos de catálogos maestros
│
├── schemas/                         # Esquemas Pydantic (Validación y Serialización)
│   ├── hotel/                       # Schemas de hoteles
│   ├── seguridad/                   # Schemas de seguridad
│   ├── reserva/                     # Schemas de reservaciones
│   ├── cliente/                     # Schemas de clientes
│   ├── empleado/                    # Schemas de empleados
│   ├── camarista/                   # Schemas de limpieza
│   ├── mantenimiento/               # Schemas de mantenimiento
│   ├── catalogos/                   # Schemas de catálogos
│   └── storage/                     # Schemas de almacenamiento
│
├── dao/                             # Capa de Acceso a Datos (Data Access Objects)
│   ├── hotel/                       # DAOs de hoteles
│   ├── seguridad/                   # DAOs de seguridad
│   ├── reserva/                     # DAOs de reservaciones
│   ├── cliente/                     # DAOs de clientes
│   ├── empleado/                    # DAOs de empleados
│   ├── camarista/                   # DAOs de limpieza
│   ├── mantenimiento/               # DAOs de mantenimiento
│   ├── catalogos/                   # DAOs de catálogos
│   └── email/                       # DAOs de email
│
├── services/                        # Capa de Lógica de Negocio
│   ├── hotel/                       # Servicios de hoteles
│   ├── seguridad/                   # Servicios de seguridad
│   ├── reserva/                     # Servicios de reservaciones
│   ├── cliente/                     # Servicios de clientes
│   ├── empleado/                    # Servicios de empleados
│   ├── camarista/                   # Servicios de limpieza
│   ├── mantenimiento/               # Servicios de mantenimiento
│   ├── catalogos/                   # Servicios de catálogos
│   ├── email/                       # Servicios de email
│   └── storage/                     # Servicios de almacenamiento (Supabase)
│
├── utils/                           # Utilidades y Helpers
│   ├── generacion_token.py          # Generación de tokens JWT
│   ├── password_generator.py        # Generación de contraseñas
│   └── rutas_imagenes.py            # Utilidades para rutas de imágenes
│
├── requirements.txt                 # Dependencias del proyecto
├── Dockerfile                       # Configuración Docker
├── docker.sh                        # Script de Docker
└── README.md                        # Documentación general
```

## 4. Patrones de Diseño Implementados

### 4.1. Singleton Pattern
- **`DatabaseConnection`** (`core/database_connection.py`): Garantiza una única instancia de conexión a la base de datos en toda la aplicación, con thread-safety.
- **`SupabaseConnection`** (`core/supabase_client.py`): Garantiza una única instancia del cliente Supabase.

### 4.2. Dependency Injection
- FastAPI utiliza dependency injection nativa para inyectar sesiones de base de datos, servicios y dependencias de seguridad.

### 4.3. Repository Pattern (DAO)
- Los DAOs encapsulan toda la lógica de acceso a datos, proporcionando una interfaz limpia para operaciones CRUD.

### 4.4. Service Layer Pattern
- Los servicios encapsulan la lógica de negocio, actuando como intermediarios entre las rutas API y los DAOs.

### 4.5. Schema Pattern (DTO)
- Los schemas Pydantic actúan como Data Transfer Objects, validando y transformando datos entre capas.

## 5. Tecnologías y Dependencias

### 5.1. Framework y Servidor
- **FastAPI 0.104.1**: Framework web moderno y rápido para APIs REST
- **Uvicorn 0.24.0**: Servidor ASGI de alto rendimiento

### 5.2. Base de Datos
- **SQLAlchemy 2.0.23**: ORM para Python
- **pyodbc 4.0.39**: Driver para conexión a SQL Server
- **SQL Server (MSSQL)**: Base de datos relacional

### 5.3. Autenticación y Seguridad
- **python-jose 3.2.0**: Implementación de JWT (JSON Web Tokens)
- **passlib 1.7.4**: Encriptación de contraseñas (Argon2)
- **HTTPBearer**: Autenticación basada en tokens Bearer

### 5.4. Validación y Configuración
- **Pydantic 2.11.9**: Validación de datos y serialización
- **pydantic-settings 2.0.3**: Configuración basada en Pydantic
- **python-dotenv 1.1.1**: Manejo de variables de entorno

### 5.5. Email y Notificaciones
- **fastapi-mail 1.4.1**: Envío de emails
- **Jinja2 3.1.2**: Motor de plantillas para emails HTML

### 5.6. Almacenamiento
- **Supabase**: Servicio de almacenamiento en la nube para imágenes y PDFs

### 5.7. Utilidades
- **aiofiles 23.2.1**: Operaciones de archivos asíncronas
- **PyYAML 6.0.1**: Procesamiento de archivos YAML

## 6. Configuración del Sistema

### 6.1. Variables de Entorno

El sistema utiliza archivos de configuración por ambiente:
- **`.development.env`**: Configuración para desarrollo
- **`.production.env`**: Configuración para producción

#### Configuración de Aplicación
- `PORT`: Puerto del servidor (default: 8000)
- `HOST`: Host del servidor (default: 127.0.0.1)
- `API_VERSION`: Versión de la API (default: /api/v1)

#### Configuración de Base de Datos
- `SERVER`: Servidor de base de datos
- `DATABASE`: Nombre de la base de datos
- `USER_DB`: Usuario de base de datos
- `PASSWORD`: Contraseña de base de datos
- `PORT_DB`: Puerto de base de datos (default: 3306)
- `DRIVER`: Driver ODBC (default: ODBC Driver 17 for SQL Server)
- `TRUST_SERVER_CERTIFICATE`: Confiar en certificado del servidor

#### Configuración de Autenticación
- `SECRET_KEY`: Clave secreta para JWT
- `ALGORITHM`: Algoritmo de encriptación (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Tiempo de expiración del token (default: 30)

#### Configuración de Email
- `SmtpServer`: Servidor SMTP (default: smtp.gmail.com)
- `SmtpPort`: Puerto SMTP (default: 587)
- `FromEmail`: Email remitente
- `FromPassword`: Contraseña del email remitente
- `EnableSsl`: Habilitar SSL

#### Configuración de Supabase
- `SUPABASE_URL`: URL del proyecto Supabase
- `SUPABASE_ANON_KEY`: Clave anónima de Supabase
- `SUPABASE_SERVICE_KEY`: Clave de servicio de Supabase
- `SUPABASE_BUCKET_IMAGES`: Bucket para imágenes
- `SUPABASE_BUCKET_PDFS`: Bucket para PDFs
- `SUPABASE_PUBLIC_BASE_URL`: URL pública base para acceso a archivos

## 7. Seguridad

### 7.1. Autenticación
- **JWT (JSON Web Tokens)**: Sistema de autenticación basado en tokens
- **HTTPBearer**: Esquema de autenticación para endpoints protegidos
- **Encriptación de contraseñas**: Uso de Argon2 para hash de contraseñas

### 7.2. CORS (Cross-Origin Resource Sharing)
- Configurado para permitir todos los orígenes (`*`) en desarrollo
- Configurable por ambiente para producción

### 7.3. Validación de Datos
- Validación automática con Pydantic en todos los endpoints
- Validación de tipos, rangos y formatos

## 8. Manejo de Archivos y Almacenamiento

### 8.1. Supabase Storage
- Almacenamiento de imágenes de hoteles, habitaciones, limpieza, mantenimiento e incidencias
- Almacenamiento de PDFs
- Generación de URLs públicas para acceso a archivos

### 8.2. Estructura de Almacenamiento
- **Bucket de Imágenes**: Almacena todas las imágenes del sistema
- **Bucket de PDFs**: Almacena documentos PDF
- Organización por tipo de entidad (hotel, habitacion, limpieza, etc.)

## 9. Sistema de Email

### 9.1. Configuración SMTP
- Soporte para múltiples proveedores SMTP (Gmail, Outlook, etc.)
- Configuración de TLS/SSL
- Plantillas HTML personalizables

### 9.2. Plantillas de Email
- Sistema de plantillas basado en Jinja2
- Plantillas personalizables con branding de InnPulse360
- Soporte para múltiples tipos de emails (bienvenida, reset de contraseña, notificaciones, etc.)

## 10. Versionado de API

- El sistema utiliza versionado de API mediante prefijos (`/api/v1`)
- Facilita la evolución de la API sin romper compatibilidad
- Preparado para futuras versiones (v2, v3, etc.)

## 11. Manejo de Errores

### 11.1. HTTP Exceptions
- Uso de `HTTPException` de FastAPI para errores HTTP estándar
- Códigos de estado apropiados (400, 401, 404, 500, etc.)
- Mensajes de error descriptivos

### 11.2. Validación de Errores
- Errores de validación automáticos de Pydantic
- Respuestas estructuradas con detalles de validación

## 12. Escalabilidad y Rendimiento

### 12.1. Connection Pooling
- Uso de SQLAlchemy connection pooling
- Configuración optimizada para aplicaciones pequeñas/medianas

### 12.2. Async/Await
- FastAPI soporta operaciones asíncronas
- Preparado para operaciones I/O asíncronas

### 12.3. Paginación
- Implementación de paginación en endpoints de listado
- Parámetros `skip` y `limit` para control de resultados

## 13. Testing y Calidad

### 13.1. Type Hints
- Uso extensivo de type hints en todo el código
- Mejora la mantenibilidad y detecta errores temprano

### 13.2. Documentación Automática
- FastAPI genera documentación automática (Swagger/OpenAPI)
- Disponible en `/docs` y `/redoc`

## 14. Dockerización

- **Dockerfile**: Configuración para containerización
- **docker.sh**: Script para facilitar operaciones Docker
- Preparado para despliegue en contenedores

## 15. Principios de Diseño Aplicados

### 15.1. SOLID
- **Single Responsibility**: Cada clase tiene una responsabilidad única
- **Dependency Inversion**: Dependencias inyectadas, no hardcodeadas
- **Open/Closed**: Extensible sin modificar código existente

### 15.2. Clean Architecture
- Separación clara de capas
- Independencia de frameworks
- Testabilidad mejorada

### 15.3. DRY (Don't Repeat Yourself)
- Reutilización de código mediante servicios y utilidades
- Evita duplicación de lógica

## 16. Flujo de Autenticación

```
1. Cliente envía credenciales → POST /api/v1/usuarios/login
2. Servicio valida credenciales
3. Si válido → Genera JWT token
4. Cliente almacena token
5. Cliente envía token en header Authorization: Bearer <token>
6. Middleware valida token en cada request
7. Si válido → Permite acceso al endpoint
8. Si inválido → Retorna 401 Unauthorized
```

## 17. Consideraciones de Producción

### 17.1. Variables de Entorno
- **NUNCA** commitear archivos `.env` con credenciales reales
- Usar secretos gestionados en producción (Azure Key Vault, AWS Secrets Manager, etc.)

### 17.2. CORS
- Configurar orígenes específicos en producción (no usar `*`)

### 17.3. Logging
- Implementar sistema de logging estructurado
- Niveles de log apropiados (DEBUG, INFO, WARNING, ERROR)

### 17.4. Monitoreo
- Implementar health checks
- Métricas de rendimiento
- Alertas de errores

## 18. Extensibilidad Futura

El sistema está preparado para:
- Implementación de caché (Redis)
- Procesamiento asíncrono de tareas (Celery, RabbitMQ)
- WebSockets para notificaciones en tiempo real
- Integración con sistemas de pago
- Reportes y analytics avanzados
- Sistema de notificaciones push

---

**Última actualización**: Diciembre 2024
**Versión del Sistema**: 1.0.0


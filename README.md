# InnPulse360 API

Una API REST moderna construida con FastAPI y SQLAlchemy para la gestión de usuarios en el sistema InnPulse360.

## 📋 Descripción

Esta aplicación proporciona una API RESTful completa para operaciones CRUD (Crear, Leer, Actualizar, Eliminar) de usuarios. Está diseñada siguiendo principios de arquitectura limpia con separación clara de responsabilidades en capas.

## 🏗️ Arquitectura

El proyecto sigue una arquitectura en capas bien definida:

```
app/
├── api/           # Capa de presentación (FastAPI routers)
│   └── v1/        # Versionado de API
├── core/          # Configuración y servicios core
├── models/        # Modelos de base de datos (SQLAlchemy)
├── schemas/       # Esquemas Pydantic para validación
├── dao/           # Data Access Objects (repositorios)
└── services/      # Lógica de negocio
```

### Capas de la Arquitectura

- **Capa API**: Endpoints REST, manejo de requests/responses
- **Capa Service**: Lógica de negocio, validaciones, transformación de datos
- **Capa DAO**: Acceso a datos, operaciones CRUD puras
- **Capa Model**: Definición de entidades de base de datos
- **Capa Schema**: Validación y serialización de datos
- **Capa Core**: Configuración, conexiones, utilidades

### Flujo de Datos
```
API → Service → DAO → Database
Response ← Schema ← Model ←
```

### Explicación del Flujo

1. **API Layer** (`app/api/`): Recibe requests HTTP, valida entrada con Pydantic
2. **Service Layer** (`app/services/`): Contiene lógica de negocio, validaciones específicas
3. **DAO Layer** (`app/dao/`): Maneja operaciones CRUD puras con la base de datos
4. **Model Layer** (`app/models/`): Define estructura de tablas con SQLAlchemy
5. **Schema Layer** (`app/schemas/`): Convierte datos para responses JSON
6. **Core Layer** (`app/core/`): Configuraciones globales y conexiones

### Ejemplo de Flujo Completo

```python
# 1. Request llega a endpoint
POST /api/v1/users/ → create_user() en users.py

# 2. Validación automática con Pydantic
user: UserCreate = UserCreate(name="Juan", email="juan@email.com")

# 3. Lógica de negocio en Service
service.create_user(user)  # Validar email único

# 4. Operación de base de datos en DAO
dao.create_user(user)  # INSERT INTO users...

# 5. Respuesta formateada con Schema
return User.from_orm(db_user)  # JSON response
```

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.11+
- SQL Server (o SQLite para desarrollo)

### Instalación

1. **Clona el repositorio**
   ```bash
   git clone <repository-url>
   cd app-interface-InnPulse360
   ```

2. **Instala dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura la base de datos**
    - Edita el archivo `.env`:
      ```
      DATABASE_URL=mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server
      ```
    - Para desarrollo con SQLite:
      ```
      DATABASE_URL=sqlite:///./app.db
      ```

4. **Ejecuta la aplicación**
   ```bash
   python main.py
   ```

5. **Accede a la documentación**
   - API Docs (Swagger): http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 📚 API Endpoints

### Usuarios

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/users/` | Lista usuarios (con paginación) |
| GET | `/api/v1/users/{user_id}` | Obtener usuario específico |
| POST | `/api/v1/users/` | Crear nuevo usuario |
| PUT | `/api/v1/users/{user_id}` | Actualizar usuario |
| DELETE | `/api/v1/users/{user_id}` | Eliminar usuario |

### Ejemplos de Uso

#### Crear Usuario
```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{"name": "Juan Pérez", "email": "juan@example.com"}'
```

#### Listar Usuarios
```bash
curl -X GET "http://localhost:8000/api/v1/users/?skip=0&limit=10"
```

#### Obtener Usuario Específico
```bash
curl -X GET "http://localhost:8000/api/v1/users/1"
```

## 🛠️ Tecnologías

- **FastAPI**: Framework web moderno y rápido para APIs
- **SQLAlchemy**: ORM para Python con soporte completo para bases de datos
- **Pydantic**: Validación de datos y configuración
- **Uvicorn**: Servidor ASGI de alto rendimiento
- **SQL Server**: Base de datos relacional (configurable)
- **Docker**: Containerización de la aplicación

## 📁 Estructura del Proyecto

```
.
├── main.py                 # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias Python
├── Dockerfile             # Configuración Docker
├── .env                   # Variables de entorno
├── README.md              # Esta documentación
└── app/
    ├── __init__.py
    ├── api/
    │   ├── __init__.py    # Aplicación FastAPI principal
    │   └── v1/
    │       ├── __init__.py # Router v1
    │       └── users.py    # Endpoints de usuarios
    ├── core/
    │   ├── __init__.py
    │   ├── config.py      # Configuración de aplicación
    │   └── database.py    # Configuración de base de datos
    ├── models/
    │   ├── __init__.py
    │   └── user.py        # Modelo User SQLAlchemy
    ├── schemas/
    │   ├── __init__.py
    │   └── user.py        # Esquemas Pydantic
    ├── dao/
    │   ├── __init__.py
    │   └── user_dao.py    # Data Access Object para usuarios
    └── services/
        ├── __init__.py
        └── user_service.py # Servicio de lógica de negocio
```

## 🔧 Configuración

### Variables de Entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `DATABASE_URL` | URL de conexión a base de datos | `mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server` |

### Base de Datos

La aplicación soporta múltiples motores de base de datos:

- **SQL Server** (recomendado para producción)
- **PostgreSQL** (configurable)
- **SQLite** (para desarrollo y pruebas)
- **MySQL/MariaDB** (configurable)

#### Configuración para SQL Server

1. **Instalar ODBC Driver**:
   - Descargar e instalar "ODBC Driver 17 for SQL Server" desde Microsoft
   - Para Windows: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

2. **Configurar conexión** en `.env`:
   ```
   DATABASE_URL=mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server
   ```

3. **Crear base de datos**:
   ```sql
   CREATE DATABASE InnPulse360;
   ```

#### Configuraciones alternativas:

**SQLite (desarrollo)**:
```
DATABASE_URL=sqlite:///./app.db
```

**PostgreSQL**:
```
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## 🐳 Docker

### Construir y Ejecutar con Docker

```bash
# Construir imagen
docker build -t innpulse360-api .

# Ejecutar contenedor
docker run -p 8000:8000 innpulse360-api
```

## 🧪 Validaciones y Reglas de Negocio

### Usuarios
- **Email único**: No se permiten emails duplicados
- **Campos requeridos**: `name` y `email` son obligatorios
- **Formato email**: Validación automática de formato de email

## 📖 Documentación Adicional

### Puntos de Interés del Código

- **Separación de responsabilidades**: Cada capa tiene una función específica
- **Inyección de dependencias**: Uso de FastAPI's dependency injection
- **Validación automática**: Pydantic maneja validación de entrada/salida
- **Transacciones**: Manejo automático de transacciones de base de datos
- **Type hints**: Anotaciones de tipo completas para mejor mantenibilidad

### Extensiones Futuras

- Autenticación y autorización (JWT, OAuth2)
- Paginación avanzada
- Filtros y búsqueda
- Caché (Redis)
- Logging estructurado
- Tests unitarios e integración
- Migraciones de base de datos (Alembic)
- API versioning avanzado

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas:
- Email: soporte@innpulse360.com
- Documentación: http://localhost:8000/docs (cuando la app esté ejecutándose)

---

**InnPulse360** - Transformando la gestión de usuarios con tecnología moderna.
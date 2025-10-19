# InnPulse360 API

Una API REST moderna construida con FastAPI para la gestión de hoteles en el sistema InnPulse360.

## 📋 Descripción

Esta aplicación proporciona una API RESTful para operaciones relacionadas con hoteles. Está diseñada siguiendo principios de arquitectura limpia con separación clara de responsabilidades en capas, preparada para expandirse con funcionalidades CRUD completas.

## 🏗️ Arquitectura

El proyecto sigue una arquitectura modular preparada para escalar:

```
app/
├── api/           # Capa de presentación (FastAPI routers)
│   └── v1/        # Versionado de API
├── core/          # Configuración y servicios core
├── models/        # Modelos de datos (preparado para SQLAlchemy)
├── schemas/       # Esquemas Pydantic para validación
├── dao/           # Data Access Objects (solo operaciones de tipo CRUD)
├── services/      # Lógica de negocio
└── utils/         # Utilidades y helpers
```

### Arquitectura Actual

- **Capa API**: Endpoints REST básicos para hoteles
- **Capa Core**: Configuración de la aplicación y manejo de entornos
- **Capa de Configuración**: Gestión de variables de entorno por ambiente

### Flujo de Datos Actual
```
API → Core → Response
```

### Estructura Preparada para Escalabilidad

El proyecto está estructurado para crecer con:
- **Modelos de datos** para entidades de hoteles
- **Servicios de negocio** para lógica compleja
- **DAOs** para acceso a base de datos
- **Schemas** para validación de datos
- **Utilidades** para funciones auxiliares

## 📋 Diferencia entre Models y Schemas

### Models (`app/models/`)
Los **Models** representan la estructura de la base de datos y son utilizados por SQLAlchemy:

```python
# Ejemplo: app/models/hotel.py
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Hotel(Base):
    __tablename__ = "hotels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    price_per_night = Column(Float, nullable=False)
    rating = Column(Float, default=0.0)
```

**Características de Models:**
- ✅ Definen la estructura de tablas en la base de datos
- ✅ Manejan relaciones entre entidades (foreign keys, etc.)
- ✅ Usados por SQLAlchemy para crear/migrar esquemas de BD
- ✅ Contienen validaciones de nivel de base de datos
- ✅ Persisten datos en la BD

### Schemas (`app/schemas/`)
Los **Schemas** definen la estructura de datos para la API REST usando Pydantic:

```python
# Ejemplo: app/schemas/hotel.py
from pydantic import BaseModel, Field
from typing import Optional

class HotelBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    location: str = Field(..., min_length=1, max_length=200)
    price_per_night: float = Field(..., gt=0)
    rating: Optional[float] = Field(None, ge=0, le=5)

class HotelCreate(HotelBase):
    pass  # Hereda todos los campos de HotelBase

class HotelUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    location: Optional[str] = Field(None, min_length=1, max_length=200)
    price_per_night: Optional[float] = Field(None, gt=0)
    rating: Optional[float] = Field(None, ge=0, le=5)

class Hotel(HotelBase):
    id: int
    
    class Config:
        from_attributes = True  # Permite conversión desde SQLAlchemy models
```

**Características de Schemas:**
- ✅ Validan datos de entrada de la API
- ✅ Serializan datos de salida para JSON
- ✅ Documentan automáticamente la API (Swagger/OpenAPI)
- ✅ Permiten diferentes estructuras para crear/actualizar/leer
- ✅ Validaciones de tipo y formato automáticas

### Flujo de Datos: Model ↔ Schema

```python
# 1. Request JSON → Schema (validación)
hotel_data = HotelCreate(name="Hotel Plaza", location="Madrid", price_per_night=150.0)

# 2. Schema → Model (para guardar en BD)
db_hotel = Hotel(**hotel_data.dict())
db.add(db_hotel)
db.commit()

# 3. Model → Schema (para respuesta JSON)
return Hotel.from_orm(db_hotel)
```

### Ejemplo de Endpoint Actual

```python
# 1. Request llega a endpoint
GET /api/v1/hotel/ → get_hotels() en routes_hotel.py

# 2. Respuesta directa
return {"message": "Hotel get request"}
```

## Inicio Rápido

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

3. **Configura las variables de entorno**
   - Para desarrollo, asegúrate de tener el archivo `.development.env`
   - Para producción, usa el archivo `.production.env`

4. **Ejecuta la aplicación**
   ```bash
   python app/main.py
   ```

5. **Accede a la documentación**
   - API Docs (Swagger): http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 📚 API Endpoints

### Hoteles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Endpoint de bienvenida |
| GET | `/api/v1/hotel/` | Obtener información de hoteles |

### Ejemplos de Uso

#### Obtener Hoteles
```bash
curl -X GET "http://localhost:8000/api/v1/hotel/"
```

#### Endpoint de Bienvenida
```bash
curl -X GET "http://localhost:8000/"
```

## 🛠️ Tecnologías

- **FastAPI**: Framework web moderno y rápido para APIs
- **Uvicorn**: Servidor ASGI de alto rendimiento
- **Python-dotenv**: Manejo de variables de entorno
- **Docker**: Containerización de la aplicación

## 📁 Estructura del Proyecto

```
.
├── app/
│   ├── __init__.py
│   ├── main.py            # Punto de entrada de la aplicación
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py # Router v1
│   │       └── routes_hotel.py # Endpoints de hoteles
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py      # Configuración de aplicación
│   │   └── database.py    # Configuración de base de datos
│   ├── models/
│   │   └── __init__.py
│   ├── schemas/
│   │   └── __init__.py
│   ├── dao/
│   │   └── __init__.py
│   ├── services/
│   │   └── __init__.py
│   ├── utils/
│   └── views/
├── requirements.txt        # Dependencias Python
├── Dockerfile             # Configuración Docker
├── .development.env       # Variables de entorno para desarrollo
├── .production.env        # Variables de entorno para producción
└── README.md              # Esta documentación
```

## 🔧 Configuración

### Variables de Entorno

La aplicación utiliza archivos de configuración específicos para diferentes entornos:

#### Desarrollo (`.development.env`)
```
PORT=8000
HOST=127.0.0.1
API_VERSION=/api/v1
```

#### Producción (`.production.env`)
```
PORT=8000
API_VERSION=/v1
```

### Configuración de la Aplicación

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `PORT` | Puerto del servidor | `8000` |
| `HOST` | Host del servidor | `127.0.0.1` |
| `API_VERSION` | Versión de la API | `/api/v1` |

La aplicación automáticamente carga el archivo `.development.env` si existe, de lo contrario carga `.production.env`.

## 🐳 Docker

### Construir y Ejecutar con Docker

```bash
# Construir imagen
docker build -t innpulse360-api .

# Ejecutar contenedor
docker run -p 8000:8000 innpulse360-api
```

## 🧪 Estado Actual y Funcionalidades

### Hoteles
- **Endpoint básico**: Disponible endpoint GET para obtener información de hoteles
- **Configuración flexible**: Sistema de configuración por ambientes (desarrollo/producción)
- **Arquitectura escalable**: Estructura preparada para implementar funcionalidades CRUD completas

## 📖 Documentación Adicional

### Puntos de Interés del Código

- **Separación de responsabilidades**: Cada capa tiene una función específica
- **Inyección de dependencias**: Uso de FastAPI's dependency injection
- **Validación automática**: Pydantic maneja validación de entrada/salida
- **Transacciones**: Manejo automático de transacciones de base de datos
- **Type hints**: Anotaciones de tipo completas para mejor mantenibilidad

### Extensiones Futuras

- **Modelos de datos**: Implementación de modelos SQLAlchemy para hoteles
- **CRUD completo**: Operaciones Create, Read, Update, Delete para hoteles
- **Validaciones**: Esquemas Pydantic para validación de datos de hoteles
- **Base de datos**: Integración con SQLAlchemy y migraciones
- **Autenticación**: Sistema de autenticación y autorización
- **Filtros y búsqueda**: Búsqueda avanzada de hoteles por ubicación, precio, etc.
- **Caché**: Implementación de Redis para mejorar rendimiento
- **Logging**: Sistema de logging estructurado
- **Tests**: Suite de tests unitarios e integración
- **API versioning**: Manejo avanzado de versiones de API

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas, consulta la documentación de la API:
- Documentación interactiva: http://localhost:8000/docs (cuando la app esté ejecutándose)
- ReDoc: http://localhost:8000/redoc

---

**InnPulse360** - Transformando la gestión de hoteles con tecnología moderna.
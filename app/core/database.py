"""
Módulo de configuración de base de datos y gestión de sesiones.

Este módulo configura el engine de SQLAlchemy, la fábrica de sesiones, y proporciona
una función de inyección de dependencias para sesiones de base de datos en FastAPI.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
"""
Engine de base de datos SQLAlchemy.

Creado con pool_pre_ping=True para asegurar que las conexiones sean válidas antes de usarlas.
Usa la URL de base de datos desde la configuración de settings.
"""

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""
Fábrica de sesiones SQLAlchemy.

Configurada para no auto-commitear o auto-flushear cambios, proporcionando control completo
sobre el manejo de transacciones.
"""

Base = declarative_base()
"""
Clase base para todos los modelos de base de datos.

Todos los modelos SQLAlchemy deben heredar de esta clase Base para ser registrados
con el sistema declarativo.
"""


def get_db():
    """
    Función de dependencia para FastAPI para proporcionar sesiones de base de datos.

    Produce una sesión de base de datos que se cierra automáticamente después del uso.
    Usada como dependencia en las funciones de ruta de FastAPI.

    Produce:
        Session: Sesión de base de datos SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
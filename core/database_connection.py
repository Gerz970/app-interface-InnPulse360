"""
Implementación del patrón Singleton para conexión a base de datos
Garantiza una única instancia de conexión en toda la aplicación
"""

import threading
from typing import Optional
from sqlalchemy import create_engine, Engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from .config import DatabaseSettings


class DatabaseConnection:
    """
    Clase Singleton para manejar la conexión a la base de datos
    
    Características del patrón Singleton:
    - Una sola instancia en toda la aplicación
    - Thread-safe (seguro para múltiples hilos)
    - Lazy initialization (se crea solo cuando se necesita)
    - Control de acceso global
    """
    
    _instance: Optional['DatabaseConnection'] = None
    _lock = threading.Lock()  # Para thread-safety
    
    def __new__(cls) -> 'DatabaseConnection':
        """
        Implementación del patrón Singleton
        """
        if cls._instance is None:
            with cls._lock:
                # Verificar nuevamente dentro del lock
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """
        Inicialización que solo ocurre una vez
        """
        if self._initialized:
            return
            
        self._engine: Optional[Engine] = None
        self._session_factory: Optional[sessionmaker] = None
        self._database_settings = DatabaseSettings()
        self._initialized = True
    
    @property
    def engine(self) -> Engine:
        """
        Propiedad que retorna el engine de SQLAlchemy
        Se crea solo cuando se accede por primera vez (Lazy initialization)
        """
        if self._engine is None:
            self._engine = self._create_engine()
        return self._engine
    
    @property
    def session_factory(self) -> sessionmaker:
        """
        Propiedad que retorna la factory de sesiones
        """
        if self._session_factory is None:
            self._session_factory = sessionmaker(
                bind=self.engine,
                autocommit=False,
                autoflush=False
            )
        return self._session_factory
    
    def _create_engine(self) -> Engine:
        """
        Crea el engine de SQLAlchemy basado en la configuración
        """
        try:
            # Construir URL de conexión para SQL Server
            connection_string = self._build_connection_string()
            
            # Crear engine con configuración optimizada para SQL Server
            # QueuePool es más adecuado para aplicaciones web con múltiples requests concurrentes
            engine = create_engine(
                connection_string,
                poolclass=QueuePool,
                pool_size=10,          # Número de conexiones a mantener en el pool
                max_overflow=20,       # Máximo de conexiones adicionales que se pueden crear
                pool_pre_ping=True,    # Verificar conexión antes de usar (importante para SQL Server)
                pool_recycle=3600,     # Reciclar conexiones después de 1 hora (evita conexiones stale)
                echo=False,            # Cambiar a True para debug SQL
                future=True            # Usar SQLAlchemy 2.0 style
            )
            
            print(f"Conexión a base de datos establecida: {self._database_settings.database}")
            return engine
            
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            raise
    
    def _build_connection_string(self) -> str:
        """
        Construye la cadena de conexión para SQL Server
        """
        # Convertir el booleano a 'yes' o 'no' para ODBC Driver
        trust_cert = "yes" if self._database_settings.trust_server_certificate else "no"
        
        # Parámetros adicionales para SQL Server/pyodbc que ayudan a evitar problemas de conexión
        # MARS (Multiple Active Result Sets) permite múltiples consultas en la misma conexión
        # pero puede causar problemas, así que lo deshabilitamos explícitamente
        return (
            f"mssql+pyodbc://{self._database_settings.username}:"
            f"{self._database_settings.password}@"
            f"{self._database_settings.server}:"
            f"{self._database_settings.port}/"
            f"{self._database_settings.database}"
            f"?driver={self._database_settings.driver.replace(' ', '+')}"
            f"&TrustServerCertificate={trust_cert}"
            f"&MARS_Connection=No"  # Deshabilitar MARS para evitar conflictos
        )
    
    def get_session(self) -> Session:
        """
        Obtiene una nueva sesión de base de datos
        IMPORTANTE: Siempre cerrar la sesión después de usarla
        """
        return self.session_factory()
    
    def get_engine(self) -> Engine:
        """
        Obtiene el engine de la base de datos
        """
        return self.engine
    
    def test_connection(self) -> bool:
        """
        Prueba la conexión a la base de datos
        """
        try:
            with self.get_session() as session:
                session.execute(text("SELECT 1"))
                print("Conexión a base de datos exitosa")
                return True
        except Exception as e:
            print(f"Error al probar conexión: {e}")
            return False
    
    def close_connection(self):
        """
        Cierra la conexión a la base de datos
        """
        if self._engine:
            self._engine.dispose()
            print("Conexión a base de datos cerrada")
    
    def __del__(self):
        """
        Destructor para limpiar recursos
        """
        self.close_connection()


# Instancia global de la conexión (Singleton)
db_connection = DatabaseConnection()


def get_database_session():
    """
    Función helper para obtener una sesión de base de datos
    Útil para usar con FastAPI dependency injection
    
    Usa yield para asegurar que la sesión se cierre correctamente
    después de que se complete la operación, incluso en operaciones asíncronas
    """
    session = db_connection.get_session()
    try:
        yield session
    finally:
        session.close()


def get_database_engine() -> Engine:
    """
    Función helper para obtener el engine de base de datos
    """
    return db_connection.get_engine()

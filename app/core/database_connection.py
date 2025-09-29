"""
Implementación del patrón Singleton para conexión a base de datos
Garantiza una única instancia de conexión en toda la aplicación
"""

import threading
from typing import Optional
from sqlalchemy import create_engine, Engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
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
            
            # Crear engine con configuración optimizada
            engine = create_engine(
                connection_string,
                poolclass=StaticPool,  # Pool estático para aplicaciones pequeñas
                pool_pre_ping=True,    # Verificar conexión antes de usar
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
        return (
            f"mssql+pyodbc://{self._database_settings.username}:"
            f"{self._database_settings.password}@"
            f"{self._database_settings.server}:"
            f"{self._database_settings.port}/"
            f"{self._database_settings.database}"
            f"?driver={self._database_settings.driver.replace(' ', '+')}"
            f"&TrustServerCertificate={self._database_settings.trust_server_certificate}"
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


def get_database_session() -> Session:
    """
    Función helper para obtener una sesión de base de datos
    Útil para usar con FastAPI dependency injection
    """
    return db_connection.get_session()


def get_database_engine() -> Engine:
    """
    Función helper para obtener el engine de base de datos
    """
    return db_connection.get_engine()

"""
Implementación del patrón Singleton para conexión a Supabase
Garantiza una única instancia de cliente en toda la aplicación
"""

import threading
from typing import Optional
from supabase import create_client, Client
from .config import SupabaseSettings


class SupabaseConnection:
    """
    Clase Singleton para manejar la conexión a Supabase
    
    Características del patrón Singleton:
    - Una sola instancia en toda la aplicación
    - Thread-safe (seguro para múltiples hilos)
    - Lazy initialization (se crea solo cuando se necesita)
    - Control de acceso global
    """
    
    _instance: Optional['SupabaseConnection'] = None
    _lock = threading.Lock()  # Para thread-safety
    
    def __new__(cls) -> 'SupabaseConnection':
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
            
        self._client: Optional[Client] = None
        self._settings = SupabaseSettings()
        self._initialized = True
    
    @property
    def client(self) -> Client:
        """
        Propiedad que retorna el cliente de Supabase
        Se crea solo cuando se accede por primera vez (Lazy initialization)
        """
        if self._client is None:
            if not self._settings.url or not self._settings.default_service_key:
                raise ValueError(
                    "Configuración de Supabase incompleta. "
                    "Verifica SUPABASE_URL y SUPABASE_SERVICE_KEY o SUPABASE_ANON_KEY en el archivo .env"
                )
            self._client = create_client(
                self._settings.url,
                self._settings.default_service_key
            )
        return self._client
    
    def test_connection(self) -> bool:
        """
        Prueba la conexión a Supabase
        """
        try:
            # Intentar listar buckets para verificar la conexión
            self.client.storage.list_buckets()
            print("Conexión a Supabase exitosa")
            return True
        except Exception as e:
            print(f"Error al probar conexión a Supabase: {e}")
            return False


# Instancia global de la conexión (Singleton)
supabase_connection = SupabaseConnection()


def get_supabase_client() -> Client:
    """
    Función helper para obtener el cliente de Supabase
    Útil para usar con FastAPI dependency injection
    """
    return supabase_connection.client


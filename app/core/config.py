"""
Módulo de configuración de la aplicación.

Este módulo maneja todas las configuraciones de la aplicación usando BaseSettings de Pydantic,
permitiendo configuración a través de variables de entorno y archivo .env.
"""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Clase de configuraciones de la aplicación.

    Usa BaseSettings de Pydantic para leer automáticamente desde variables de entorno
    y archivo .env. Proporciona valores por defecto para configuración de base de datos.

    Atributos:
        database_url (str): URL de conexión a base de datos. Por defecto SQL Server.
                            Se puede cambiar a SQLite, PostgreSQL u otras bases de datos.
    """
    database_url: str = "mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server"
    # Para desarrollo con SQLite: "sqlite:///./app.db"
    # Para PostgreSQL: "postgresql://user:password@localhost/dbname"

    class Config:
        """Configuración de Pydantic para carga de settings."""
        env_file = ".env"


settings = Settings()
"""
Instancia global de configuraciones.

Esta instancia se usa en toda la aplicación para acceder a los valores de configuración.
Carga automáticamente desde variables de entorno y archivo .env.
"""
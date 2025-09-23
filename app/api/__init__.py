"""
Módulo principal de aplicación FastAPI.

Este módulo crea y configura la instancia principal de aplicación FastAPI,
incluyendo todas las versiones de API y configuraciones globales.
"""

from fastapi import FastAPI

from .v1 import router as v1_router

app = FastAPI(title="InnPulse360 API", version="1.0.0")
"""
Instancia principal de aplicación FastAPI.

Configurada con título y versión para la API InnPulse360.
Incluye todos los routers de versiones de API.
"""

app.include_router(v1_router, prefix="/api/v1")
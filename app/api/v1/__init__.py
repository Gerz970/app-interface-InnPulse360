"""
Módulo de router de API Versión 1.

Este módulo agrupa todos los endpoints de API v1 en un solo router,
proporcionando un punto centralizado para el manejo de la API versión 1.
"""

from fastapi import APIRouter

from .users import router as users_router

router = APIRouter()
"""
Router principal para API versión 1.

Incluye todos los endpoints v1 con prefijos y tags apropiados.
"""
router.include_router(users_router, prefix="/users", tags=["users"])
from fastapi import APIRouter
from .routes_hotel import api_router as hotel_router
from .routes_usuario import router as usuario_router

api_router = APIRouter()

api_router.include_router(hotel_router)
api_router.include_router(usuario_router)
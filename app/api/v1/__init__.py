from fastapi import APIRouter
from .routes_hotel import api_router as hotel_router
from .routes_usuario import router as usuario_router
from .routes_roles import router as roles_router
from .routes_usuario_rol import router as usuario_rol_router
from .routes_pais import router as pais_router
from .routes_estado import router as estado_router
from .routes_tipo_habitacion import router as tipo_habitacion_router
from .routes_caracteristica import router as caracteristica_router
from .routes_tipo_habitacion_caracteristica import router as tipo_habitacion_caracteristica_router
from .routes_email import router as email_router
from .routes_empleado import api_router as empleado_router

api_router = APIRouter()


api_router.include_router(usuario_router)
api_router.include_router(roles_router)
api_router.include_router(usuario_rol_router)
api_router.include_router(hotel_router)
api_router.include_router(pais_router)
api_router.include_router(estado_router)
api_router.include_router(tipo_habitacion_router)
api_router.include_router(caracteristica_router)
api_router.include_router(tipo_habitacion_caracteristica_router)
api_router.include_router(email_router)
api_router.include_router(empleado_router)
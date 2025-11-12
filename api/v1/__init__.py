from fastapi import APIRouter
from .routes_hotel import api_router as hotel_router
from .routes_usuario import router as usuario_router
from .routes_roles import router as roles_router
from .routes_usuario_rol import router as usuario_rol_router
from .routes_modulos import router as modulos_router
from .routes_cliente import router as cliente_router
from .routes_pais import router as pais_router
from .routes_estado import router as estado_router
from .routes_tipo_habitacion import router as tipo_habitacion_router
from .routes_caracteristica import router as caracteristica_router
from .routes_tipo_habitacion_caracteristica import router as tipo_habitacion_caracteristica_router
from .routes_email import router as email_router
from .routes_empleado import api_router as empleado_router
from .routes_puesto import api_router as puesto_router
from .routes_piso import router as piso_router
from .routes_habitacion_area import router as habitacion_area_router
from .routes_periodicidad import router as periodicidad_router
from .routes_tipo_cargo import router as tipo_cargo_router
from .routes_cargo import router as cargo_router
from .routes_reservacion import router as reservacion_router
from .routes_cargo_servicio_transporte import router as cargo_servicio_transporte_router
from .routes_servicio_transporte import router as servicio_transporte_router
from .routes_mantenimiento import router as router_mantenimiento
from .routes_incidencia import router as router_incidencia
from .routes_tipo_limpieza import router as router_tipo_limpieza
from .routes_estatus_limpieza import router as router_estatus_limpieza
from .routes_limpieza import router as router_limpieza
from .routes_imagenes import router as router_imagenes
from .routes_hotel_imagenes import router as router_hotel_imagenes
from .routes_mantenimiento_imagenes import router as router_mantenimiento_imagenes
from .routes_limpieza_imagenes import router as router_limpieza_imagenes
from .routes_habitacion_imagenes import router as router_habitacion_imagenes
from .routes_tipo_habitacion_imagenes import router as router_tipo_habitacion_imagenes

api_router = APIRouter()

api_router.include_router(usuario_router)
api_router.include_router(roles_router)
api_router.include_router(usuario_rol_router)
api_router.include_router(modulos_router)
api_router.include_router(cliente_router)
api_router.include_router(hotel_router)
api_router.include_router(pais_router)
api_router.include_router(estado_router)
api_router.include_router(tipo_habitacion_router)
api_router.include_router(caracteristica_router)
api_router.include_router(tipo_habitacion_caracteristica_router)
api_router.include_router(email_router)
api_router.include_router(empleado_router)
api_router.include_router(puesto_router)
api_router.include_router(piso_router)
api_router.include_router(habitacion_area_router)
api_router.include_router(periodicidad_router)
api_router.include_router(tipo_cargo_router)
api_router.include_router(cargo_router)
api_router.include_router(reservacion_router)
api_router.include_router(servicio_transporte_router)
api_router.include_router(cargo_servicio_transporte_router)
api_router.include_router(router_mantenimiento)
api_router.include_router(router_incidencia)
api_router.include_router(router_tipo_limpieza)
api_router.include_router(router_estatus_limpieza)
api_router.include_router(router_limpieza)
api_router.include_router(router_imagenes)
api_router.include_router(router_hotel_imagenes)
api_router.include_router(router_mantenimiento_imagenes)
api_router.include_router(router_limpieza_imagenes)
api_router.include_router(router_habitacion_imagenes)
api_router.include_router(router_tipo_habitacion_imagenes)

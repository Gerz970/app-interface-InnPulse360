# controllers/servicio_transporte_controller.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from core.database_connection import get_database_session
from schemas.reserva.servicios_transporte_schema import (
    ServicioTransporteCreate,
    ServicioTransporteUpdate,
    ServicioTransporteResponse,
)
from schemas.seguridad.usuario_response import UsuarioResponse
from services.reserva.servicio_transporte_service import ServicioTransporteService
from api.v1.routes_usuario import get_current_user
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

router = APIRouter(prefix="/servicios-transporte", tags=["Servicios de Transporte"])
service = ServicioTransporteService()

@router.get("/", response_model=list[ServicioTransporteResponse])
def listar_servicios(
    db: Session = Depends(get_database_session),
    current_user: UsuarioResponse = Depends(get_current_user)
):
    """
    Lista servicios de transporte del cliente autenticado.
    Solo retorna servicios asociados a reservaciones del cliente en sesión.
    """
    return service.listar(db, usuario_id=current_user.id_usuario)

@router.get("/{id_servicio}", response_model=ServicioTransporteResponse)
def obtener_servicio(
    id_servicio: int,
    db: Session = Depends(get_database_session),
    current_user: UsuarioResponse = Depends(get_current_user)
):
    """
    Obtiene un servicio de transporte por ID.
    Valida que el servicio pertenece al cliente autenticado.
    """
    servicio = service.obtener(db, id_servicio, usuario_id=current_user.id_usuario)
    return servicio

@router.get("/empleado/{empleado_id}", response_model=list[ServicioTransporteResponse])
def obtener_por_empleado(
    empleado_id: int,
    db: Session = Depends(get_database_session),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Obtiene todos los servicios de transporte asignados a un empleado específico.
    """
    return service.obtener_por_empleado(db, empleado_id)

@router.post("/", response_model=ServicioTransporteResponse)
def crear_servicio(
    data: ServicioTransporteCreate, 
    reservacion_id: Optional[int] = Query(None, description="ID de la reservación para asociar el cargo"),
    db: Session = Depends(get_database_session), 
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Crea un servicio de transporte.
    Si se proporciona reservacion_id, también crea un cargo asociado a la reservación.
    
    Campos que NO se asignan en la creación:
    - empleado_id: Se asignará en un proceso aparte
    - calificacion_viaje: Se asignará cuando se complete el viaje
    - observaciones_empleado: Se asignará por el conductor después
    """
    # Asegurar que estos campos sean None al crear
    # Usar model_dump si está disponible (Pydantic v2), sino usar dict (Pydantic v1)
    try:
        servicio_dict = data.model_dump(exclude_unset=True)
    except AttributeError:
        servicio_dict = data.dict(exclude_unset=True)
    
    # Forzar que estos campos sean None al crear
    servicio_dict['empleado_id'] = None
    servicio_dict['calificacion_viaje'] = None
    servicio_dict['observaciones_empleado'] = None
    
    # Crear el servicio de transporte con los datos limpios
    servicio_data = ServicioTransporteCreate(**servicio_dict)
    servicio = service.crear(db, servicio_data)
    
    # Si viene reservacion_id, crear el cargo asociado
    if reservacion_id:
        from services.reserva.cargo_service import CargoService
        from services.reserva.tipo_cargo_service import TipoCargoService
        from schemas.reserva.cargos_schema import CargoCreate
        
        cargo_service = CargoService()
        tipo_cargo_service = TipoCargoService()
        
        # Buscar el tipo de cargo "Transporte" por nombre (case-insensitive)
        tipos_cargo = tipo_cargo_service.listar_todos(db)
        tipo_transporte = next(
            (tipo for tipo in tipos_cargo if tipo.nombre_cargo.lower() == "transporte"), 
            None
        )
        
        if not tipo_transporte:
            raise HTTPException(
                status_code=404, 
                detail="Tipo de cargo 'Transporte' no encontrado en el sistema"
            )
        
        # Crear el cargo asociado a la reservación
        cargo_data = CargoCreate(
            reservacion_id=reservacion_id,
            concepto=f"Transporte - {data.destino}",
            costo_unitario=data.costo_viaje,  # Usar el costo calculado del servicio
            cantidad=1,
            tipo_id=tipo_transporte.id_tipo
        )
        
        # Crear cargo y asociarlo con el servicio de transporte
        cargo_service.crearCargoConServicio(db, cargo_data, servicio.id_servicio_transporte)
    
    return servicio

@router.put("/{id_servicio}", response_model=ServicioTransporteResponse)
def actualizar_servicio(id_servicio: int, data: ServicioTransporteUpdate, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    servicio = service.actualizar(db, id_servicio, data)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio

@router.delete("/{id_servicio}")
def eliminar_servicio(id_servicio: int, db: Session = Depends(get_database_session), credentials: HTTPAuthorizationCredentials = Depends(security)):
    servicio = service.eliminar(db, id_servicio)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return {"message": "Servicio eliminado correctamente"}

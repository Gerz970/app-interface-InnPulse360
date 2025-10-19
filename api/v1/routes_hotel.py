from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List
from sqlalchemy.orm import Session
from core.config import Settings
from core.database_connection import get_database_session
from schemas.hotel import HotelCreate, HotelUpdate, HotelResponse
from services.hotel.hotel_service import HotelService
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# Crear instancia de settings
settings = Settings()

# Configurar seguridad
security = HTTPBearer()


api_router = APIRouter(prefix="/hotel", tags=["hotel"])


def get_hotel_service(db: Session = Depends(get_database_session)) -> HotelService:
    """
    Dependency para obtener una instancia del servicio de hotel
    
    Args:
        db (Session): Sesión de base de datos (inyectada por FastAPI)
        
    Returns:
        HotelService: Instancia del servicio de hotel
    """
    try:
        return HotelService(db)
    finally:
        db.close()


@api_router.get("/", response_model=List[HotelResponse])
async def get_hotels(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    service: HotelService = Depends(get_hotel_service),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Obtener lista de todos los hoteles con paginación
    
    Args:
        skip (int): Número de registros a saltar (para paginación)
        limit (int): Número máximo de registros a retornar
        service (HotelService): Servicio de hotel (inyectado)
    
    Returns:
        List[HotelResponse]: Lista de todos los hoteles
        
    Raises:
        HTTPException: 500 si hay un error en el servidor
    """
    try:
        hoteles = service.obtener_todos_los_hoteles(skip=skip, limit=limit)
        return hoteles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener hoteles: {str(e)}"
        )


@api_router.get("/{hotel_id}", response_model=HotelResponse)
async def get_hotel(
    hotel_id: int,
    service: HotelService = Depends(get_hotel_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Obtener un hotel específico por ID
    
    Args:
        hotel_id (int): ID del hotel a buscar
        service (HotelService): Servicio de hotel (inyectado)
        
    Returns:
        HotelResponse: Datos del hotel
        
    Raises:
        HTTPException: 404 si el hotel no existe
        HTTPException: 500 si hay un error en el servidor
    """
    try:
        hotel = service.obtener_hotel_por_id(hotel_id)
        
        if not hotel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Hotel con ID {hotel_id} no encontrado"
            )
        
        return hotel
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener hotel: {str(e)}"
        )


@api_router.post("/", response_model=HotelResponse, status_code=status.HTTP_201_CREATED)
async def create_hotel(
    hotel: HotelCreate,
    service: HotelService = Depends(get_hotel_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Crear un nuevo hotel
    
    Args:
        hotel (HotelCreate): Datos del hotel a crear
        service (HotelService): Servicio de hotel (inyectado)
        
    Returns:
        HotelResponse: Hotel creado con ID generado
        
    Raises:
        HTTPException: 400 si los datos son inválidos
        HTTPException: 500 si hay un error en el servidor
    """
    try:
        hotel_creado = service.crear_hotel(hotel)
        return hotel_creado
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear hotel: {str(e)}"
        )


@api_router.put("/{hotel_id}", response_model=HotelResponse)
async def update_hotel(
    hotel_id: int,
    hotel_update: HotelUpdate,
    service: HotelService = Depends(get_hotel_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Actualizar un hotel existente (actualización parcial)
    
    Args:
        hotel_id (int): ID del hotel a actualizar
        hotel_update (HotelUpdate): Datos a actualizar (parciales)
        service (HotelService): Servicio de hotel (inyectado)
        
    Returns:
        HotelResponse: Hotel actualizado
        
    Raises:
        HTTPException: 404 si el hotel no existe
        HTTPException: 400 si los datos son inválidos
        HTTPException: 500 si hay un error en el servidor
    """
    try:
        hotel_actualizado = service.actualizar_hotel(hotel_id, hotel_update)
        
        if not hotel_actualizado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Hotel con ID {hotel_id} no encontrado"
            )
        
        return hotel_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar hotel: {str(e)}"
        )


@api_router.delete("/{hotel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hotel(
    hotel_id: int,
    service: HotelService = Depends(get_hotel_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Eliminar un hotel
    
    Args:
        hotel_id (int): ID del hotel a eliminar
        service (HotelService): Servicio de hotel (inyectado)
        
    Raises:
        HTTPException: 404 si el hotel no existe
        HTTPException: 500 si hay un error en el servidor
    """
    try:
        eliminado = service.eliminar_hotel(hotel_id)
        
        if not eliminado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Hotel con ID {hotel_id} no encontrado"
            )
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar hotel: {str(e)}"
        )


# Rutas adicionales para búsquedas específicas

@api_router.get("/buscar/nombre/{nombre}", response_model=List[HotelResponse])
async def buscar_por_nombre(
    nombre: str,
    service: HotelService = Depends(get_hotel_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Buscar hoteles por nombre (búsqueda parcial)
    
    Args:
        nombre (str): Nombre o parte del nombre a buscar
        service (HotelService): Servicio de hotel (inyectado)
        
    Returns:
        List[HotelResponse]: Lista de hoteles encontrados
    """
    try:
        hoteles = service.buscar_por_nombre(nombre)
        return hoteles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar hoteles: {str(e)}"
        )


@api_router.get("/pais/{id_pais}", response_model=List[HotelResponse])
async def obtener_por_pais(
    id_pais: int,
    service: HotelService = Depends(get_hotel_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Obtener todos los hoteles de un país
    
    Args:
        id_pais (int): ID del país
        service (HotelService): Servicio de hotel (inyectado)
        
    Returns:
        List[HotelResponse]: Lista de hoteles del país
    """
    try:
        hoteles = service.obtener_por_pais(id_pais)
        return hoteles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener hoteles por país: {str(e)}"
        )


@api_router.get("/estrellas/{numero_estrellas}", response_model=List[HotelResponse])
async def obtener_por_estrellas(
    numero_estrellas: int,
    service: HotelService = Depends(get_hotel_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Obtener hoteles por número de estrellas
    
    Args:
        numero_estrellas (int): Número de estrellas (1-5)
        service (HotelService): Servicio de hotel (inyectado)
        
    Returns:
        List[HotelResponse]: Lista de hoteles
    """
    try:
        hoteles = service.obtener_por_estrellas(numero_estrellas)
        return hoteles
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener hoteles por estrellas: {str(e)}"
        )


from fastapi import APIRouter, HTTPException, status
from typing import List
from core.config import Settings
from schemas.hotel import HotelCreate, HotelUpdate, HotelResponse

# Crear instancia de settings
settings = Settings()

api_router = APIRouter(prefix="/hotel", tags=["hotel"])


@api_router.get("/", response_model=List[HotelResponse])
async def get_hotels():
    """
    Obtener lista de todos los hoteles
    
    Returns:
        List[HotelResponse]: Lista de todos los hoteles
    """
    # TODO: Implementar consulta a base de datos
    pass


@api_router.get("/{hotel_id}", response_model=HotelResponse)
async def get_hotel(hotel_id: int):
    """
    Obtener un hotel específico por ID
    
    Args:
        hotel_id (int): ID del hotel a buscar
        
    Returns:
        HotelResponse: Datos del hotel
        
    Raises:
        HTTPException: 404 si el hotel no existe
    """
    # TODO: Implementar consulta a base de datos
    pass


@api_router.post("/", response_model=HotelResponse, status_code=status.HTTP_201_CREATED)
async def create_hotel(hotel: HotelCreate):
    """
    Crear un nuevo hotel
    
    Args:
        hotel (HotelCreate): Datos del hotel a crear
        
    Returns:
        HotelResponse: Hotel creado con ID generado
    """
    # TODO: Implementar inserción en base de datos
    pass


@api_router.put("/{hotel_id}", response_model=HotelResponse)
async def update_hotel(hotel_id: int, hotel_update: HotelUpdate):
    """
    Actualizar un hotel existente
    
    Args:
        hotel_id (int): ID del hotel a actualizar
        hotel_update (HotelUpdate): Datos a actualizar (parciales)
        
    Returns:
        HotelResponse: Hotel actualizado
        
    Raises:
        HTTPException: 404 si el hotel no existe
    """
    # TODO: Implementar actualización en base de datos
    pass


@api_router.delete("/{hotel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hotel(hotel_id: int):
    """
    Eliminar un hotel
    
    Args:
        hotel_id (int): ID del hotel a eliminar
        
    Raises:
        HTTPException: 404 si el hotel no existe
    """
    # TODO: Implementar eliminación en base de datos
    pass


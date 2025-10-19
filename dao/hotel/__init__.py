"""
DAO para módulo de hotel
Contiene DAOs para gestión hotelera
"""

from .dao_caracteristica import CaracteristicaDAO
from .dao_hotel import HotelDAO
from .dao_tipo_habitacion import TipoHabitacionDAO
from .dao_tipo_habitacion_caracteristica import TipoHabitacionCaracteristicaDAO

__all__ = [
    "CaracteristicaDAO", 
    "HotelDAO", 
    "TipoHabitacionDAO", 
    "TipoHabitacionCaracteristicaDAO"
]

"""
Archivo que importa todos los modelos de catálogos en el orden correcto
para que las relaciones funcionen correctamente
"""

# Importar la base primero
from .base import Base

# Importar modelos en el orden correcto para las relaciones
from .pais_model import Pais
from .estado_model import Estado
from .tipo_habitacion_model import TipoHabitacion
from .caracteristica_model import Caracteristica
from .tipo_habitacion_caracteristica_model import TipoHabitacionCaracteristica

# Exportar todo
__all__ = [
    "Base",
    "Pais", 
    "Estado", 
    "TipoHabitacion", 
    "Caracteristica", 
    "TipoHabitacionCaracteristica"
]

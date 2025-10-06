"""
Archivo que importa todos los modelos de catálogos en el orden correcto
para que las relaciones funcionen correctamente
"""

# Importar la base primero
from core.base import Base

# Importar modelos en el orden correcto para las relaciones
from .pais_model import Pais
from .estado_model import Estado

# Exportar todo
__all__ = [
    "Base",
    "Pais", 
    "Estado"
]

from core.base import Base

# Importar todos los modelos para que las relaciones funcionen correctamente
from .pais_model import Pais
from .estado_model import Estado

__all__ = ["Base", "Pais", "Estado"]

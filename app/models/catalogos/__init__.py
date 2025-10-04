from .base import Base

# Importar todos los modelos para que las relaciones funcionen correctamente
from .pais_model import Pais
from .estado_model import Estado
from .tipo_habitacion_model import TipoHabitacion
from .caracteristica_model import Caracteristica
from .tipo_habitacion_caracteristica_model import TipoHabitacionCaracteristica

__all__ = ["Base", "Pais", "Estado", "TipoHabitacion", "Caracteristica", "TipoHabitacionCaracteristica"]

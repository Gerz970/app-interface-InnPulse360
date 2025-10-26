# Importar todos los modelos para que las relaciones funcionen correctamente
from .catalogos.models import *
from .seguridad.usuario_model import Usuario
from .seguridad.roles_model import Roles
from .hotel.hotel_model import Hotel
from .hotel.tipo_habitacion_model import TipoHabitacion
from .hotel.caracteristica_model import Caracteristica
from .hotel.tipo_habitacion_caracteristica_model import TipoHabitacionCaracteristica
from .empleados import *
from .cliente import *
from .reserva import *

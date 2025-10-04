# Importar todos los modelos para que las relaciones funcionen correctamente
from .catalogos.models import *
from .seguridad.usuario_model import Usuario
from .seguridad.roles_model import Roles
from .seguridad.rol_usuario_model import RolUsuario
from .hotel.hotel_model import Hotel

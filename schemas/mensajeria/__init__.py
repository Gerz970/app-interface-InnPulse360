# Schemas del módulo de Mensajería
from .conversacion_schema import (
    ConversacionCreate,
    ConversacionCreateClienteAdmin,
    ConversacionCreateEmpleadoEmpleado,
    ConversacionUpdate,
    ConversacionResponse,
    ConversacionListResponse,
    UsuarioDisponibleResponse
)
from .mensaje_schema import (
    MensajeCreate,
    MensajeResponse
)
from .mensaje_adjunto_schema import (
    MensajeAdjuntoResponse
)

# Reconstruir modelos para resolver referencias circulares en Pydantic v2
# Esto es necesario cuando los modelos se referencian entre sí
# Importante: reconstruir en el orden correcto (dependencias primero)
MensajeAdjuntoResponse.model_rebuild()
MensajeResponse.model_rebuild()
ConversacionResponse.model_rebuild()
ConversacionListResponse.model_rebuild()
UsuarioDisponibleResponse.model_rebuild()

__all__ = [
    'ConversacionCreate',
    'ConversacionCreateClienteAdmin',
    'ConversacionCreateEmpleadoEmpleado',
    'ConversacionUpdate',
    'ConversacionResponse',
    'ConversacionListResponse',
    'UsuarioDisponibleResponse',
    'MensajeCreate',
    'MensajeResponse'
]


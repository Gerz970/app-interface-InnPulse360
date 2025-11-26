# Schemas del módulo de Mensajería
from .conversacion_schema import (
    ConversacionCreate,
    ConversacionCreateClienteAdmin,
    ConversacionCreateEmpleadoEmpleado,
    ConversacionUpdate,
    ConversacionResponse,
    ConversacionListResponse
)
from .mensaje_schema import (
    MensajeCreate,
    MensajeResponse
)

__all__ = [
    'ConversacionCreate',
    'ConversacionCreateClienteAdmin',
    'ConversacionCreateEmpleadoEmpleado',
    'ConversacionUpdate',
    'ConversacionResponse',
    'ConversacionListResponse',
    'MensajeCreate',
    'MensajeResponse'
]


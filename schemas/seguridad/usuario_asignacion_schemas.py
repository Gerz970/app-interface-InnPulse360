from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UsuarioAsignacionBase(BaseModel):
    """
    Schema base para asignación de usuario
    """
    usuario_id: int = Field(..., gt=0, description="ID del usuario")
    tipo_asignacion: int = Field(..., ge=1, le=2, description="1=Empleado, 2=Cliente")
    empleado_id: Optional[int] = Field(None, description="ID del empleado (si tipo=1)")
    cliente_id: Optional[int] = Field(None, description="ID del cliente (si tipo=2)")
    
    class Config:
        from_attributes = True


class UsuarioAsignacionCreate(UsuarioAsignacionBase):
    """
    Schema para crear asignación
    """
    pass


class UsuarioAsignacionResponse(BaseModel):
    """
    Schema para respuesta de asignación
    """
    id_asignacion: int = Field(..., description="ID de la asignación")
    usuario_id: int = Field(..., description="ID del usuario")
    empleado_id: Optional[int] = Field(None, description="ID del empleado")
    cliente_id: Optional[int] = Field(None, description="ID del cliente")
    tipo_asignacion: int = Field(..., description="1=Empleado, 2=Cliente")
    tipo_asignacion_texto: str = Field(..., description="Empleado o Cliente")
    fecha_asignacion: datetime = Field(..., description="Fecha de asignación")
    estatus: int = Field(..., description="Estatus de la asignación")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_asignacion": 1,
                "usuario_id": 10,
                "empleado_id": None,
                "cliente_id": 5,
                "tipo_asignacion": 2,
                "tipo_asignacion_texto": "Cliente",
                "fecha_asignacion": "2024-01-15T10:30:00",
                "estatus": 1
            }
        }


class UsuarioConAsignacionResponse(BaseModel):
    """
    Schema para usuario con información de su asignación
    """
    id_usuario: int
    login: str
    correo_electronico: str
    estatus_id: int
    password_temporal: bool
    password_expira: Optional[datetime]
    
    # Asignación
    tiene_asignacion: bool = Field(default=False)
    tipo_asignacion: Optional[str] = Field(None, description="Empleado o Cliente")
    cliente_id: Optional[int] = None
    cliente_nombre: Optional[str] = None
    empleado_id: Optional[int] = None
    
    class Config:
        from_attributes = True


class UsuarioEmpleadoAsociacionRequest(BaseModel):
    """
    Schema para solicitar asociación de usuario con empleado
    """
    usuario_id: int = Field(..., gt=0, description="ID del usuario existente")
    empleado_id: int = Field(..., gt=0, description="ID del empleado existente")


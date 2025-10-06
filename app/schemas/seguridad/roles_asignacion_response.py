from pydantic import BaseModel, Field


class RolesAsignacionResponse(BaseModel):
    """
    Schema para respuestas de Roles Asignados a usuarios

    {
        "usuario_id": assignment.id_usuario,
        "rol_id": assignment.id_rol,
        "usuario_login": assignment.login,
        "usuario_email": assignment.correo_electronico,
        "rol_nombre": assignment.rol,
        "rol_descripcion": assignment.descripcion
    }
    """
    usuario_id: int = Field(
        ...,
        description="ID único del usuario",
        example=1
    )
    
    usuario_login: str = Field(
        ...,
        description="Login del usuario",
        example="juan.perez"
    )
    
    rol_id: int = Field(
        ...,
        description="ID del rol",
        example=1
    )
    
    usuario_email: str = Field(
        ...,
        description="Email del usuario",
        example="juan.perez@gmail.com"
    )
    
    rol_nombre: str = Field(
        ...,
        description="Nombre del rol",
        example="Administrador"
    )
    
    rol_descripcion: str = Field(
        ...,
        description="Descripción del rol",
        example="Rol con permisos completos del sistema"
    )
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "usuario_id": 1,
                "usuario_login": "juan.perez",
                "rol_id": 1,
                "usuario_email": "juan.perez@gmail.com",
                "rol_nombre": "Administrador",
                "rol_descripcion": "Rol con permisos completos del sistema"
            }
        }
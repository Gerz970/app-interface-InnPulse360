from pydantic import BaseModel, Field, EmailStr


class RecuperarPasswordRequest(BaseModel):
    """
    Schema para solicitar recuperación de contraseña
    """
    correo_electronico: EmailStr = Field(..., description="Correo electrónico del usuario")
    
    class Config:
        json_schema_extra = {
            "example": {
                "correo_electronico": "usuario@email.com"
            }
        }


class RecuperarPasswordResponse(BaseModel):
    """
    Respuesta de recuperación de contraseña
    SEGURIDAD: La contraseña temporal NO se devuelve en la respuesta,
    se envía directamente al correo electrónico del usuario
    """
    success: bool = Field(..., description="Si la solicitud fue procesada exitosamente")
    mensaje: str = Field(..., description="Mensaje descriptivo")
    email_enviado: bool = Field(..., description="Si se envió email con contraseña temporal")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "mensaje": "Si el correo existe en nuestro sistema, se ha enviado una contraseña temporal.",
                "email_enviado": True
            }
        }


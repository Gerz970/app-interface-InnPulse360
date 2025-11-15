from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from schemas.cliente.cliente_formulario import ClienteFormularioData


class VerificarDisponibilidadRequest(BaseModel):
    """
    Schema para verificar disponibilidad de login y correo
    """
    login: str = Field(..., min_length=1, max_length=25, description="Login a verificar")
    correo_electronico: str = Field(..., min_length=1, max_length=50, description="Correo a verificar")
    
    class Config:
        json_schema_extra = {
            "example": {
                "login": "cliente123",
                "correo_electronico": "cliente@email.com"
            }
        }


class ClienteEncontradoInfo(BaseModel):
    """
    Información básica del cliente encontrado
    """
    id_cliente: int
    nombre_razon_social: str
    rfc: Optional[str]
    tipo_persona: int
    correo_electronico: str
    
    class Config:
        from_attributes = True


class VerificarDisponibilidadResponse(BaseModel):
    """
    Respuesta de verificación de disponibilidad
    """
    login_disponible: bool = Field(..., description="Si el login está disponible")
    correo_en_clientes: bool = Field(..., description="Si el correo existe en tabla clientes")
    cliente: Optional[ClienteFormularioData] = Field(None, description="Datos completos del cliente si existe")
    puede_registrar: bool = Field(..., description="Si puede continuar con el registro")
    usuario_ya_existe: bool = Field(default=False, description="Si el cliente ya tiene un usuario asociado con ese correo")
    mensaje: str = Field(..., description="Mensaje descriptivo")
    
    class Config:
        json_schema_extra = {
            "example": {
                "login_disponible": True,
                "correo_en_clientes": True,
                "cliente": {
                    "tipo_persona": 1,
                    "documento_identificacion": 123456789,
                    "nombre_razon_social": "Juan Pérez González",
                    "apellido_paterno": "Pérez",
                    "apellido_materno": "González",
                    "rfc": "PEGJ800101XXX",
                    "curp": "PEGJ800101HDFRRN01",
                    "telefono": "5512345678",
                    "direccion": "Calle Principal 123, Col. Centro",
                    "pais_id": 1,
                    "estado_id": 15,
                    "correo_electronico": "cliente@email.com",
                    "representante": "Juan Pérez",
                    "id_estatus": 1
                },
                "puede_registrar": True,
                "usuario_ya_existe": False,
                "mensaje": "Login disponible. Se encontró cliente con este correo."
            }
        }


class RegistroClienteRequest(BaseModel):
    """
    Schema para registro de usuario-cliente
    """
    login: str = Field(..., min_length=1, max_length=25, description="Login del usuario")
    correo_electronico: str = Field(..., min_length=1, max_length=50, description="Correo electrónico")
    password: Optional[str] = Field(None, min_length=6, description="Contraseña (opcional, se genera si no se envía)")
    cliente_id: int = Field(..., gt=0, description="ID del cliente a asociar")
    
    class Config:
        json_schema_extra = {
            "example": {
                "login": "cliente123",
                "correo_electronico": "cliente@email.com",
                "password": None,
                "cliente_id": 123
            }
        }


class RegistroClienteResponse(BaseModel):
    """
    Respuesta de registro de usuario-cliente
    SEGURIDAD: La contraseña temporal NO se devuelve en la respuesta, 
    se envía directamente al correo electrónico del cliente
    """
    usuario_creado: bool = Field(..., description="Si el usuario fue creado")
    id_usuario: int = Field(..., description="ID del usuario creado")
    login: str = Field(..., description="Login del usuario")
    correo_electronico: str = Field(..., description="Correo del usuario")
    
    # Asignación
    cliente_asociado: ClienteEncontradoInfo = Field(..., description="Cliente asociado")
    rol_asignado: str = Field(..., description="Rol asignado (Cliente)")
    
    # Password temporal - Solo indicadores, NO se devuelve la contraseña
    password_temporal_generada: bool = Field(..., description="Si se generó password temporal")
    email_enviado: bool = Field(..., description="Si se envió email con credenciales")
    
    mensaje: str = Field(..., description="Mensaje de éxito")
    
    class Config:
        json_schema_extra = {
            "example": {
                "usuario_creado": True,
                "id_usuario": 45,
                "login": "cliente123",
                "correo_electronico": "cliente@email.com",
                "cliente_asociado": {
                    "id_cliente": 123,
                    "nombre_razon_social": "Juan Pérez González",
                    "rfc": "PEGJ800101XXX",
                    "tipo_persona": 1,
                    "correo_electronico": "cliente@email.com"
                },
                "rol_asignado": "Cliente",
                "password_temporal_generada": True,
                "email_enviado": True,
                "mensaje": "Usuario creado exitosamente. Se han enviado las credenciales al correo electrónico proporcionado."
            }
        }


class CambiarPasswordTemporalRequest(BaseModel):
    """
    Schema para cambiar password temporal
    """
    login: str = Field(..., description="Login del usuario")
    password_actual: str = Field(..., min_length=6, description="Password temporal actual")
    password_nueva: str = Field(..., min_length=6, description="Nueva contraseña")
    password_confirmacion: str = Field(..., min_length=6, description="Confirmación de nueva contraseña")
    
    @field_validator('password_confirmacion')
    @classmethod
    def passwords_match(cls, v, info):
        if 'password_nueva' in info.data and v != info.data['password_nueva']:
            raise ValueError('Las contraseñas no coinciden')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "login": "cliente123",
                "password_actual": "A1b2C3d4E5f6",
                "password_nueva": "MiNuevaPassword123",
                "password_confirmacion": "MiNuevaPassword123"
            }
        }


class CambiarPasswordTemporalResponse(BaseModel):
    """
    Respuesta de cambio de password temporal
    """
    success: bool = Field(..., description="Si el cambio fue exitoso")
    mensaje: str = Field(..., description="Mensaje descriptivo")
    requiere_login: bool = Field(default=True, description="Si debe iniciar sesión nuevamente")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "mensaje": "Contraseña actualizada exitosamente",
                "requiere_login": True
            }
        }

from pydantic import BaseModel, Field
from typing import Optional

class HabitacionAreaBase(BaseModel):
    piso_id: int = Field(..., description="ID del piso al que pertenece")
    tipo_habitacion_id: int = Field(..., description="ID del tipo de habitación")
    nombre_clave: str = Field(..., max_length=25, description="Nombre o clave del área")
    descripcion: str = Field(..., max_length=150, description="Descripción del área")
    estatus_id: int = Field(..., description="Estatus del registro")

class HabitacionAreaCreate(HabitacionAreaBase):
    """Esquema para creación"""
    pass
    class Config:
        json_schema_extra = {
            "example": {
                "piso_id": 2,
                "tipo_habitacion_id": 3,
                "nombre_clave": "Suite Presidencial",
                "descripcion": "Habitación de lujo con vista al mar",
                "estatus_id": 1
            }
        }

class HabitacionAreaUpdate(BaseModel):
    """Esquema para actualización parcial"""
    piso_id: Optional[int]= None
    tipo_habitacion_id: Optional[int]= None
    nombre_clave: Optional[str]= None
    descripcion: Optional[str]= None
    estatus_id: Optional[int]= None

    class Config:
        json_schema_extra = {
            "example": {
                "nombre_clave": "Suite Presidencial",
                "descripcion": "Habitación de lujo con vista al mar",
            }
        }

class HabitacionAreaResponse(HabitacionAreaBase):
    id_habitacion_area: int
    piso_id: int 
    tipo_habitacion_id: int 
    nombre_clave: str 
    descripcion: str 
    estatus_id: int 

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_habitacion_area": 1,
                "piso_id": 2,
                "tipo_habitacion_id": 3,
                "nombre_clave": "Suite Presidencial",
                "descripcion": "Habitación de lujo con vista al mar",
                "estatus_id": 1
            }
        }

class HabitacionAreaConEstadoResponse(BaseModel):
    """Schema para habitación con información de estado"""
    id_habitacion_area: int
    piso_id: int
    tipo_habitacion_id: int
    nombre_clave: str
    descripcion: str
    estatus_id: int
    tiene_reservacion_activa: bool
    tiene_limpieza_pendiente: bool
    tiene_limpieza_en_proceso: bool
    puede_seleccionarse: bool

    class Config:
        from_attributes = True
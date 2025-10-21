from pydantic import BaseModel, Field
from typing import Optional

class PisoBase(BaseModel):
    id_hotel: int = Field(..., description="ID del hotel al que pertenece el piso")
    numero_pisos: int = Field(None, description="Número de pisos o nivel")
    nombre: str = Field(..., max_length=50)
    descripcion: str = Field(..., max_length=150)
    estatus_id: int = Field(..., description="Estatus del piso")

class PisoCreate(PisoBase):
    id_hotel: int = Field(..., description="ID del hotel al que pertenece el piso")
    numero_pisos: int = Field(None, description="Número de pisos o nivel")
    nombre: str = Field(..., max_length=50)
    descripcion: str = Field(..., max_length=150)
    estatus_id: int = Field(..., description="Estatus del piso")

    class Config:
        json_schema_extra = {
            "example": {
                "id_hotel": 2,
                "numero_pisos": 3,
                "nombre": "Piso Ejecutivo",
                "descripcion": "Área de suites de lujo",
                "estatus_id": 1
            }
        }

class PisoUpdate(BaseModel):
    numero_pisos: Optional[int] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    estatus_id: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Piso Ejecutivo",
                "descripcion": "Área de suites de lujo",
            }
        }

class PisoResponse(PisoBase):
    id_piso: int
    id_hotel: int
    numero_pisos: int
    nombre: str
    descripcion: str
    estatus_id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_piso": 1,
                "id_hotel": 2,
                "numero_pisos": 3,
                "nombre": "Piso Ejecutivo",
                "descripcion": "Área de suites de lujo",
                "estatus_id": 1
            }
        }

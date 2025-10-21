from pydantic import BaseModel
from typing import Optional

class PeriodicidadBase(BaseModel):
    periodicidad: str
    descripcion: Optional[str] = None

class PeriodicidadCreate(PeriodicidadBase):
    pass

class PeriodicidadUpdate(PeriodicidadBase):
    id_estatus: Optional[bool] = True

class PeriodicidadResponse(PeriodicidadBase):
    id_periodicidad: int
    id_estatus: bool

    class Config:
        from_attributes = True
        json_schema_extra = {
            "periodicidad": {
                "id_periodicidad": 1,
                "periodicidad": "Temporal",
                "descripcion": "Tiempo indefinido",
                "id_estatus": 1
            }
        }

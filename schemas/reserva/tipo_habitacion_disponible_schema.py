from pydantic import BaseModel, Field
from typing import List
from ..hotel.tipo_habitacion_schemas import TipoHabitacionResponse

class TipoHabitacionDisponibleResponse(BaseModel):
    """Schema para tipos de habitación disponibles con cantidad"""
    tipo_habitacion: TipoHabitacionResponse = Field(..., description="Información del tipo de habitación")
    cantidad_disponible: int = Field(..., ge=0, description="Cantidad de habitaciones disponibles de este tipo")
    
    class Config:
        json_schema_extra = {
            "example": {
                "tipo_habitacion": {
                    "id_tipoHabitacion": 1,
                    "clave": "SGL",
                    "tipo_habitacion": "Individual",
                    "precio_unitario": 1000,
                    "periodicidad": {
                        "id_periodicidad": 1,
                        "periodicidad": "Temporal",
                        "descripcion": "Tiempo indefinido",
                        "id_estatus": 1
                    },
                    "estatus_id": 1,
                    "url_foto_perfil": "https://tu-proyecto.supabase.co/storage/v1/object/public/images/tipo_habitacion/1/default.jpg",
                    "galeria_tipo_habitacion": [
                        "https://tu-proyecto.supabase.co/storage/v1/object/public/images/tipo_habitacion/1/galeria/img_1_item1.jpg",
                        "https://tu-proyecto.supabase.co/storage/v1/object/public/images/tipo_habitacion/1/galeria/img_1_item2.jpg"
                    ]
                },
                "cantidad_disponible": 5
            }
        }


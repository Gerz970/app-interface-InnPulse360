from pydantic import BaseModel, Field
from decimal import Decimal
from pydantic import BaseModel
from .tipo_cargo_schema import TipoCargoResponse
class CargoBase(BaseModel):
    reservacion_id: int = Field(
        ...,
        description= "Reservación asociada",
        example= 1
    )

    concepto: str = Field(
        min_length=1,
        max_length=250,
        description="Nombre del cargo",
        example="Bebida"
    )

    costo_unitario: Decimal = Field(
        ..., 
        ge=0, 
        decimal_places=2, 
        description="Costo del servicio"
    )

    cantidad: int = Field(
        ...,
        description= "Cantidad del producto",
        example= 1
    )

    tipo_id: int= Field(
        ...,
        description= "Id del tipo de producto",
        example= 1
    )

class CargoCreate(CargoBase):
    pass

class CargoResponse(CargoBase):
    id_cargo: int
    tipo_cargo : TipoCargoResponse

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example" : {
                "id_cargo": 1,
                "reservacion_id": 1,
                "concepto": "Estacionamiento",
                "costo_unitario": 100.00,
                "cantidad": 1,
                "tipo_cargo": {
                    "nombre_cargo": "Restaurante",
                    "descripcion": "Uso del servicio de buffet",
                    "id_estatus": 1,
                    "id_tipo": 1                           
                }
            }
        }
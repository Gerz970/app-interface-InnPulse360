from pydantic import BaseModel
from typing import Optional

class DomicilioBase(BaseModel):
    id_domicilio: Optional[int] = None
    domicilio_completo: str
    codigo_postal: str

    class Config: 
        from_attributes = True
        json_schema_extra = {
            "domicilio": {
                "id_domicilio": 1,
                "domicilio_completo": "Calle Los Olivos #123, Col. Centro, CDMX",
                "codigo_postal": "06000"
            }
        }
        

class DomicilioUpdate(BaseModel):
    domicilio_completo: str
    codigo_postal: str
    class Config: 
        json_schema_extra = {
            "domicilio": {
                "domicilio_completo": "Calle Los Olivos #123, Col. Centro, CDMX",
                "codigo_postal": "06000"
            }
        }
from pydantic import BaseModel
from typing import Optional

class DomicilioBase(BaseModel):
    id_domicilio: Optional[int] = None
    domicilio_completo: str
    codigo_postal: str

    class Config: 
        from_attributes = True
from pydantic import BaseModel

class DomicilioBase(BaseModel):
    domicilio_completo: str
    codigo_postal: str
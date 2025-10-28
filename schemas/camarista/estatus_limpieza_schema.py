from pydantic import BaseModel

# Modelo base (compartido)
class EstatusLimpiezaBase(BaseModel):
    nombre: str

# Para crear nuevos registros
class EstatusLimpiezaCreate(EstatusLimpiezaBase):
    pass

# Para actualizar (todos los campos opcionales)
class EstatusLimpiezaUpdate(BaseModel):
    nombre: str | None = None
    id_estatus: int | None = None

# Para devolver datos al cliente
class EstatusLimpiezaResponse(EstatusLimpiezaBase):
    id_estatus_limpieza: int
    id_estatus: int

    class Config:
        from_attributes = True

from sqlalchemy.orm import Session
from dao.hotel.dao_piso import PisoDAO
from models.hotel.piso_model import Piso
from schemas.hotel.piso_schema import PisoCreate, PisoUpdate

class PisoService:
    def __init__(self, db: Session):
        self.dao = PisoDAO(db)

    def listar_pisos(self, hotel_id: int):
        return self.dao.get_all(hotel_id)

    def obtener_piso(self, id_piso: int):
        piso = self.dao.get_by_id(id_piso)
        if not piso:
            raise ValueError("Piso no encontrado")
        return piso

    def crear_piso(self, piso_data: PisoCreate):
        nuevo_piso = Piso(**piso_data.model_dump())
        return self.dao.create(nuevo_piso)

    def actualizar_piso(self, id_piso: int, piso_data: PisoUpdate):
        data_dict = piso_data.model_dump(exclude_unset=True)
        piso = self.dao.update(id_piso, data_dict)
        if not piso:
            raise ValueError("Piso no encontrado para actualizar")
        return piso

    def eliminar_piso(self, id_piso: int):
        piso = self.dao.delete(id_piso)
        if not piso:
            raise ValueError("Piso no encontrado para eliminar")
        return piso

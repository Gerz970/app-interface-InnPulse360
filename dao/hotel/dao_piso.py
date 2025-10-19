from sqlalchemy.orm import Session
from models.hotel.piso_model import Piso
from schemas.hotel.piso_schema import PisoCreate, PisoUpdate, PisoResponse

class PisoDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, hotel_id: int):
        return (
        self.db.query(Piso)
        .filter(Piso.id_hotel == hotel_id)
        .order_by(Piso.id_piso)
        .all()
        )

    def get_by_id(self, id_piso: int):
        return self.db.query(Piso).filter(Piso.id_piso == id_piso).first()

    def create(self, piso: PisoCreate):
        self.db.add(piso)
        self.db.commit()
        self.db.refresh(piso)
        return piso

    def update(self, id_piso: int, data: PisoUpdate):
        piso = self.get_by_id(id_piso)
        if not piso:
            return None
        for key, value in data.items():
            setattr(piso, key, value)
        self.db.commit()
        self.db.refresh(piso)
        return piso

    def delete(self, id_piso: int):
        piso = self.get_by_id(id_piso)
        if not piso:
            return None
        
        (
            self.db.query(Piso)
            .filter(Piso.id_piso == id_piso) 
            .update({"estatus_id": 0}) # Actualiza el estatus a inactivo para baja lógica
        ) 
       
        self.db.commit()
        return piso

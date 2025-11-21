from sqlalchemy.orm import Session
from models.reserva.cargos_model import Cargo
from schemas.reserva.cargos_schema import CargoCreate
from sqlalchemy import func

class CargoDAO:

    def get_all(self, db: Session):
        """Obtiene todos los cargos"""
        return db.query(Cargo).all()

    def get_by_id(self, db: Session, id_cargo: int):
        """Obtiene un cargo por su ID"""
        return db.query(Cargo).filter(Cargo.id_cargo == id_cargo).first()

    def get_by_id_reserva(self, db: Session, id_reserva: int):
        return db.query(Cargo).filter(Cargo.reservacion_id == id_reserva).all()
    
    def create(self, db: Session, cargo_data: CargoCreate):
        """Crea un nuevo cargo"""
        nuevo_cargo = Cargo(**cargo_data.dict(exclude_unset=True))
        db.add(nuevo_cargo)
        db.commit()
        db.refresh(nuevo_cargo)
        return nuevo_cargo

    def update(self, db: Session, id_cargo: int, cargo_data: CargoCreate):
        """Actualiza un cargo existente"""
        cargo = db.query(Cargo).filter(Cargo.id_cargo == id_cargo).first()
        if not cargo:
            return None

        for key, value in cargo_data.dict(exclude_unset=True).items():
            setattr(cargo, key, value)

        db.commit()
        db.refresh(cargo)
        return cargo

    def delete(self, db: Session, id_cargo: int):
        """Elimina físicamente un cargo"""
        cargo = db.query(Cargo).filter(Cargo.id_cargo == id_cargo).first()
        if not cargo:
            return None

        db.delete(cargo)
        db.commit()
        return cargo
    
    def obtener_total_por_reserva(self, db: Session, reservacion_id:int):
        resultado = (
        db.query(
            Cargo.reservacion_id,
            func.sum(Cargo.costo_unitario).label("total")
        )
        .filter(Cargo.reservacion_id == reservacion_id)
        .group_by(Cargo.reservacion_id)
        .first()
        )

        if resultado is None:
            return None

        return {
            "reservacion_id": resultado[0],
            "total": float(resultado[1])
        }

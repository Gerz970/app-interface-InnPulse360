from sqlalchemy.orm import Session
from models.reserva.tipo_cargos_model import TipoCargo
from schemas.reserva.tipo_cargo_schema import TipoCargoCreate, TipoCargoUpdate


class TipoCargoDAO:

    def get_all(self, db: Session):
        """Obtiene todos los tipos de cargo"""
        return db.query(TipoCargo).filter(TipoCargo.id_estatus == 1).all()

    def get_by_id(self, db: Session, id_tipo: int):
        """Obtiene un tipo de cargo por su ID"""
        return db.query(TipoCargo).filter(TipoCargo.id_tipo == id_tipo).first()

    def create(self, db: Session, tipo_data: TipoCargoCreate):
        """Crea un nuevo registro de tipo de cargo"""
        nuevo_tipo = TipoCargo(**tipo_data.dict())
        db.add(nuevo_tipo)
        db.commit()
        db.refresh(nuevo_tipo)
        return nuevo_tipo

    def update(self, db: Session, id_tipo: int, tipo_data: TipoCargoUpdate):
        """Actualiza un registro existente"""
        tipo_cargo = db.query(TipoCargo).filter(TipoCargo.id_tipo == id_tipo).first()
        if not tipo_cargo:
            return None

        for key, value in tipo_data.dict(exclude_unset=True).items():
            setattr(tipo_cargo, key, value)

        db.commit()
        db.refresh(tipo_cargo)
        return tipo_cargo

    def delete(self, db: Session, id_tipo: int):
        tipo_cargo = db.query(TipoCargo).filter(TipoCargo.id_tipo == id_tipo).first()
        if not tipo_cargo:
            return None

    # Cambiar el estatus a inactivo (eliminado lógicamente)
        tipo_cargo.id_estatus = 0

        db.commit()
        db.refresh(tipo_cargo)
        return tipo_cargo


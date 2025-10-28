from sqlalchemy.orm import Session
from models.camarista.tipos_limpieza import TiposLimpieza

class TiposLimpiezaDao:

    def get_all(self, db: Session):
        return db.query(TiposLimpieza).filter(TiposLimpieza.id_estatus == 1).all()
    
    def get_by_id(self, db: Session, id_tipo_limpieza: int):
        return db.query(TiposLimpieza).filter(TiposLimpieza.id_tipo_limpieza == id_tipo_limpieza).first()
    
    
    def create(self, db: Session, tipo_limpieza: TiposLimpieza) -> TiposLimpieza:
        db.add(tipo_limpieza)
        db.commit()
        db.refresh(tipo_limpieza)
        return tipo_limpieza

    def update(self, db: Session, id_tipo_limpieza: int, data: dict) -> TiposLimpieza:
        db_tipo_limpieza = db.query(TiposLimpieza).filter(TiposLimpieza.id_tipo_limpieza == id_tipo_limpieza).first()
        if not db_tipo_limpieza:
            return None
        for key, value in data.items():
            setattr(db_tipo_limpieza, key, value)
        db.commit()
        db.refresh(db_tipo_limpieza)
        return db_tipo_limpieza

    def delete(self, db: Session, id_tipo_limpieza: int):
        db_tipo_limpieza = db.query(TiposLimpieza).filter(TiposLimpieza.id_tipo_limpieza == id_tipo_limpieza).first()
        if not db_tipo_limpieza:
            return None
        
        (
            db.query(TiposLimpieza)
            .filter(TiposLimpieza.id_tipo_limpieza == id_tipo_limpieza) 
            .update({"id_estatus": 0}) # Actualiza el estatus a inactivo para baja lógica
        ) 
        db.commit()
        db.refresh(db_tipo_limpieza)
        return db_tipo_limpieza

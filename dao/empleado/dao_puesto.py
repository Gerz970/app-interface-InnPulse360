from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.empleados.puesto_model import Puesto
from schemas.empleado.puesto_schema import PuestoCreate, PuestoUpdate, PuestoResponse

class PuestoDAO:
    __status_active__ = 1
    __status_inactive__ = 0

    def __init__(self, db_session: Session):
        self.db = db_session
    
    def create(self, puesto_data: PuestoCreate) -> Puesto:
        try:
            # Crear puesto usando **data
            db_puesto = Puesto(**puesto_data.model_dump())

            self.db.add(db_puesto)
            self.db.commit()
            self.db.refresh(db_puesto)

            return db_puesto
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_by_id(self, puesto_id: int) -> Optional[Puesto]:
        try:
            return self.db.query(Puesto).filter(Puesto.id_puesto == puesto_id).first()
        except SQLAlchemyError as e:
            raise e
        
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Puesto]:
        try:
            return (
                self.db.query(Puesto)
                .order_by(Puesto.id_puesto.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            raise e
        
    def update(self, puesto_id: int, puesto_update: PuestoUpdate)-> Optional[Puesto]:
        try:
            db_puesto = self.get_by_id(puesto_id)
            if not db_puesto:
                return None
            
            update_data = puesto_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_puesto, field, value)

            self.db.commit()
            self.db.refresh(db_puesto)
            return db_puesto
    
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def delete_logical(self, puesto_id: int) -> bool:
        try:
            db_puesto = self.get_by_id(puesto_id) 
            
            if not db_puesto:
                return False
            
            (
                self.db.query(Puesto)
                .filter(Puesto.id_puesto == puesto_id) # Filtra el hotel por su id
                .update({"estatus_id": self.__status_inactive__}) # Actualiza el estatus a inactivo para baja lógica
            ) 
            self.db.commit() # Guarda los cambios   
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    

from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError
from models.empleados.domicilio_model import Domicilio
from schemas.empleado.domicilio_base import DomicilioUpdate

class DireccionDAO:

    def __init__(self, db_session: Session):
        self.db = db_session

    def update(self, domicilio_id: int, domicilio_update: DomicilioUpdate) -> Optional[Domicilio]:
        try:
            db_domicilio = self.db.query(Domicilio).filter(Domicilio.id_domicilio == domicilio_id).first()
            if not db_domicilio:
                return None

            update_data = domicilio_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_domicilio, field, value)

            self.db.commit()
            self.db.refresh(db_domicilio)
            return db_domicilio

        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy.exc import SQLAlchemyError
from models.empleados.empleado_model import Empleado
from schemas.empleado.empleado_create import EmpleadoCreate
from schemas.empleado.empleado_update import EmpleadoUpdate
from schemas.empleado.empleado_response import EmpleadoResponse
from models.empleados.domicilio_model import Domicilio
from models.empleados.domicilio_empleado_model import DomicilioEmpleado
from models.empleados.puesto_model import Puesto
from models.hotel.hotel_model import Hotel
class EmpleadoDAO:
    __status_active__ = 1
    __status_inactive__ = 0

    def __init__(self, db_session: Session):
        self.db = db_session

    def create(self, empleado_data: EmpleadoCreate) -> Empleado:
        try:
            # Crear empleado
            db_empleado = Empleado(
                clave_empleado=empleado_data.clave_empleado,
                nombre=empleado_data.nombre,
                apellido_paterno=empleado_data.apellido_paterno,
                apellido_materno=empleado_data.apellido_materno,
                fecha_nacimiento=empleado_data.fecha_nacimiento,
                rfc=empleado_data.rfc,
                curp=empleado_data.curp,
            )
            self.db.add(db_empleado)
            self.db.flush()  # obtiene el ID antes del commit

            # Crear domicilio
            db_domicilio = Domicilio(
                domicilio_completo=empleado_data.domicilio.domicilio_completo,
                codigo_postal=empleado_data.domicilio.codigo_postal,
                estatus_id=1
            )
            self.db.add(db_domicilio)
            self.db.flush()

            # Crear relación empleado-domicilio
            relacion = DomicilioEmpleado(
                empleado_id=db_empleado.id_empleado,
                domicilio_id=db_domicilio.id_domicilio
            )
            self.db.add(relacion)

            # Relacionar con el puesto
            puesto = self.db.query(Puesto).filter(Puesto.id_puesto == empleado_data.puesto_id).first()
            if puesto:
                db_empleado.puestos.append(puesto)

            hotel = self.db.query(Hotel).filter(Hotel.id_hotel == empleado_data.hotel_id).first()
            if hotel:
                db_empleado.hoteles.append(hotel)

            # Guardar todo junto
            self.db.commit()
            self.db.refresh(db_empleado)

            return db_empleado

        except Exception as e:
            self.db.rollback()
            raise e


        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def get_all(self, hotel_id: int, skip: int = 0, limit: int = 100):
        return (
            self.db.query(Empleado)
            .options(
                joinedload(Empleado.domicilio_relacion).joinedload(DomicilioEmpleado.domicilio),
                joinedload(Empleado.puestos),
                joinedload(Empleado.hoteles)
            )
            .filter(Empleado.hoteles.any(Hotel.id_hotel == hotel_id))
            .order_by(Empleado.id_empleado)
            .offset(skip)
            .limit(limit)
            .all()
        )


    def get_by_id(self, empleado_id: int):
        empleado_db = (
            self.db.query(Empleado)
            .options(
                joinedload(Empleado.domicilio_relacion).joinedload(DomicilioEmpleado.domicilio),
                joinedload(Empleado.puestos),
                joinedload(Empleado.hoteles)                
            )
            .filter(Empleado.id_empleado == empleado_id)
            .first()
        )

        if not empleado_db:
            return None

        print("Puestos asociados:", empleado_db.puestos)  # 👈 Aquí deberías ver los puestos cargados

        # Retornar el objeto convertido a Pydantic
        return EmpleadoResponse.model_validate(empleado_db)

        
    
    def update(self, empleado_id: int, empleado_update: EmpleadoUpdate) -> Optional[Empleado]:
        try:
            db_empleado = self.db.query(Empleado).filter(Empleado.id_empleado == empleado_id).first()
            if not db_empleado:
                return None

            update_data = empleado_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_empleado, field, value)

            self.db.commit()
            self.db.refresh(db_empleado)
            return db_empleado

        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def delete(self, empleado_id: int) -> bool:
        """
        Elimina físicamente un empleado de la base de datos.
        Retorna True si se eliminó, False si no existe.
        """
        try:
            empleado = self.db.query(Empleado).filter(Empleado.id_empleado == empleado_id).first()
            if not empleado:
                raise Exception("Empleado no encontrado")
            self.db.delete(empleado)
            self.db.commit()
            return True

        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

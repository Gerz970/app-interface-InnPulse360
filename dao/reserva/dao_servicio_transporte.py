# dao/servicio_transporte_dao.py
from sqlalchemy.orm import Session, joinedload
from models.reserva.servicios_transporte_model import ServicioTransporte
from models.reserva.cargo_servicio_transporte_model import CargoServicioTransporte
from models.reserva.cargos_model import Cargo
from models.reserva.reservaciones_model import Reservacion
from schemas.reserva.servicios_transporte_schema import ServicioTransporteCreate, ServicioTransporteUpdate

class ServicioTransporteDAO:

    def get_all(self, db: Session):
        return db.query(ServicioTransporte).options(
            joinedload(ServicioTransporte.empleado)
        ).all()

    def get_by_id(self, db: Session, id_servicio: int):
        return db.query(ServicioTransporte).options(
            joinedload(ServicioTransporte.empleado)
        ).filter(ServicioTransporte.id_servicio_transporte == id_servicio).first()

    def get_all_by_cliente_id(self, db: Session, cliente_id: int):
        """
        Obtiene todos los servicios de transporte asociados a un cliente específico
        a través de la relación: ServicioTransporte → Cargo → Reservacion → Cliente
        
        Args:
            db (Session): Sesión de base de datos
            cliente_id (int): ID del cliente
            
        Returns:
            List[ServicioTransporte]: Lista de servicios de transporte del cliente
        """
        return db.query(ServicioTransporte).options(
            joinedload(ServicioTransporte.empleado)
        ).join(
            CargoServicioTransporte,
            ServicioTransporte.id_servicio_transporte == CargoServicioTransporte.servicio_transporte_id
        ).join(
            Cargo,
            CargoServicioTransporte.cargo_id == Cargo.id_cargo
        ).join(
            Reservacion,
            Cargo.reservacion_id == Reservacion.id_reservacion
        ).filter(
            Reservacion.cliente_id == cliente_id
        ).distinct().all()

    def get_by_id_and_cliente_id(self, db: Session, id_servicio: int, cliente_id: int):
        """
        Obtiene un servicio de transporte por ID validando que pertenece al cliente especificado
        
        Args:
            db (Session): Sesión de base de datos
            id_servicio (int): ID del servicio de transporte
            cliente_id (int): ID del cliente
            
        Returns:
            Optional[ServicioTransporte]: Servicio encontrado o None si no existe o no pertenece al cliente
        """
        return db.query(ServicioTransporte).options(
            joinedload(ServicioTransporte.empleado)
        ).join(
            CargoServicioTransporte,
            ServicioTransporte.id_servicio_transporte == CargoServicioTransporte.servicio_transporte_id
        ).join(
            Cargo,
            CargoServicioTransporte.cargo_id == Cargo.id_cargo
        ).join(
            Reservacion,
            Cargo.reservacion_id == Reservacion.id_reservacion
        ).filter(
            ServicioTransporte.id_servicio_transporte == id_servicio,
            Reservacion.cliente_id == cliente_id
        ).distinct().first()

    def get_all_by_empleado_id(self, db: Session, empleado_id: int):
        """
        Obtiene todos los servicios de transporte asignados a un empleado específico
        
        Args:
            db (Session): Sesión de base de datos
            empleado_id (int): ID del empleado/conductor
            
        Returns:
            List[ServicioTransporte]: Lista de servicios de transporte del empleado
        """
        return db.query(ServicioTransporte).options(
            joinedload(ServicioTransporte.empleado)
        ).filter(
            ServicioTransporte.empleado_id == empleado_id
        ).all()

    def create(self, db: Session, data: ServicioTransporteCreate):
        nuevo_servicio = ServicioTransporte(**data.dict())
        db.add(nuevo_servicio)
        db.commit()
        db.refresh(nuevo_servicio)
        # Recargar con la relación empleado para la respuesta
        return self.get_by_id(db, nuevo_servicio.id_servicio_transporte)

    def update(self, db: Session, id_servicio: int, data: ServicioTransporteUpdate):
        servicio = self.get_by_id(db, id_servicio)
        if not servicio:
            return None
        for key, value in data.dict(exclude_unset=True).items():
            setattr(servicio, key, value)
        db.commit()
        db.refresh(servicio)
        # Recargar con la relación empleado para la respuesta
        return self.get_by_id(db, id_servicio)

    def delete(self, db: Session, id_servicio: int):
        servicio = self.get_by_id(db, id_servicio)
        if not servicio:
            return None
        db.delete(servicio)
        db.commit()
        return servicio

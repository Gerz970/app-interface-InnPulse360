# services/servicio_transporte_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from dao.reserva.dao_servicio_transporte import ServicioTransporteDAO
from dao.seguridad.dao_usuario_asignacion import UsuarioAsignacionDAO
from schemas.reserva.servicios_transporte_schema import ServicioTransporteCreate, ServicioTransporteUpdate

class ServicioTransporteService:
    def __init__(self):
        self.dao = ServicioTransporteDAO()

    def listar(self, db: Session, usuario_id: int = None):
        """
        Lista servicios de transporte.
        Si se proporciona usuario_id, filtra solo los servicios del cliente asociado al usuario.
        
        Args:
            db (Session): Sesión de base de datos
            usuario_id (int, optional): ID del usuario autenticado. Si se proporciona, filtra por cliente.
            
        Returns:
            List[ServicioTransporte]: Lista de servicios de transporte
        """
        # Si no se proporciona usuario_id, retornar todos (comportamiento anterior para compatibilidad)
        if usuario_id is None:
            return self.dao.get_all(db)
        
        # Obtener cliente_id desde usuario_id
        usuario_asignacion_dao = UsuarioAsignacionDAO(db)
        asignacion = usuario_asignacion_dao.get_by_usuario_id(usuario_id)
        
        # Validar que el usuario tiene asignación a cliente
        if not asignacion:
            # Usuario sin asignación, retornar lista vacía
            return []
        
        # Validar que es tipo CLIENTE (tipo_asignacion == 2)
        if asignacion.tipo_asignacion != UsuarioAsignacionDAO.TIPO_CLIENTE:
            # No es cliente, retornar lista vacía
            return []
        
        # Obtener cliente_id
        cliente_id = asignacion.cliente_id
        if not cliente_id:
            # No tiene cliente_id asignado, retornar lista vacía
            return []
        
        # Filtrar servicios por cliente
        return self.dao.get_all_by_cliente_id(db, cliente_id)

    def obtener(self, db: Session, id_servicio: int, usuario_id: int = None):
        """
        Obtiene un servicio de transporte por ID.
        Si se proporciona usuario_id, valida que el servicio pertenece al cliente asociado al usuario.
        
        Args:
            db (Session): Sesión de base de datos
            id_servicio (int): ID del servicio de transporte
            usuario_id (int, optional): ID del usuario autenticado. Si se proporciona, valida acceso.
            
        Returns:
            Optional[ServicioTransporte]: Servicio encontrado o None
            
        Raises:
            HTTPException: Si el usuario no tiene acceso al servicio (403)
        """
        # Si no se proporciona usuario_id, usar método original (comportamiento anterior)
        if usuario_id is None:
            return self.dao.get_by_id(db, id_servicio)
        
        # Obtener cliente_id desde usuario_id
        usuario_asignacion_dao = UsuarioAsignacionDAO(db)
        asignacion = usuario_asignacion_dao.get_by_usuario_id(usuario_id)
        
        # Validar que el usuario tiene asignación a cliente
        if not asignacion:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes acceso a este servicio"
            )
        
        # Validar que es tipo CLIENTE (tipo_asignacion == 2)
        if asignacion.tipo_asignacion != UsuarioAsignacionDAO.TIPO_CLIENTE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes acceso a este servicio"
            )
        
        # Obtener cliente_id
        cliente_id = asignacion.cliente_id
        if not cliente_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes acceso a este servicio"
            )
        
        # Obtener servicio validando que pertenece al cliente
        servicio = self.dao.get_by_id_and_cliente_id(db, id_servicio, cliente_id)
        
        if not servicio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Servicio no encontrado o no tienes acceso a este servicio"
            )
        
        return servicio

    def crear(self, db: Session, data: ServicioTransporteCreate):
        return self.dao.create(db, data)

    def actualizar(self, db: Session, id_servicio: int, data: ServicioTransporteUpdate):
        return self.dao.update(db, id_servicio, data)

    def eliminar(self, db: Session, id_servicio: int):
        return self.dao.delete(db, id_servicio)

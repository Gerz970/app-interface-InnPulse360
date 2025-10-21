"""
DAO (Data Access Object) para operaciones de UsuarioAsignacion
Maneja la asociación entre usuarios y clientes/empleados
"""

from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.seguridad.usuario_asignacion_model import UsuarioAsignacion
from schemas.seguridad.usuario_asignacion_schemas import UsuarioAsignacionCreate


class UsuarioAsignacionDAO:
    """
    Clase DAO para manejar operaciones de UsuarioAsignacion
    """
    
    # Constantes de tipo de asignación
    TIPO_EMPLEADO = 1
    TIPO_CLIENTE = 2
    
    def __init__(self, db_session: Session):
        """
        Inicializa el DAO con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy
        """
        self.db = db_session
    
    def create(self, asignacion_data: UsuarioAsignacionCreate) -> UsuarioAsignacion:
        """
        Crea una nueva asignación de usuario
        
        Args:
            asignacion_data (UsuarioAsignacionCreate): Datos de la asignación
            
        Returns:
            UsuarioAsignacion: Asignación creada
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Crear asignación usando **data
            asignacion_dict = asignacion_data.model_dump()
            asignacion_dict['estatus'] = 1
            db_asignacion = UsuarioAsignacion(**asignacion_dict)
            
            self.db.add(db_asignacion)
            self.db.commit()
            self.db.refresh(db_asignacion)
            
            return db_asignacion
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def crear_asignacion_cliente(self, usuario_id: int, cliente_id: int) -> UsuarioAsignacion:
        """
        Crea una asignación de usuario con cliente
        
        Args:
            usuario_id (int): ID del usuario
            cliente_id (int): ID del cliente
            
        Returns:
            UsuarioAsignacion: Asignación creada
        """
        # Crear datos de asignación
        asignacion_data = UsuarioAsignacionCreate(
            usuario_id=usuario_id,
            empleado_id=None,
            cliente_id=cliente_id,
            tipo_asignacion=self.TIPO_CLIENTE
        )
        return self.create(asignacion_data)
    
    def crear_asignacion_empleado(self, usuario_id: int, empleado_id: int) -> UsuarioAsignacion:
        """
        Crea una asignación de usuario con empleado
        
        Args:
            usuario_id (int): ID del usuario
            empleado_id (int): ID del empleado
            
        Returns:
            UsuarioAsignacion: Asignación creada
        """
        # Crear datos de asignación
        asignacion_data = UsuarioAsignacionCreate(
            usuario_id=usuario_id,
            empleado_id=empleado_id,
            cliente_id=None,
            tipo_asignacion=self.TIPO_EMPLEADO
        )
        return self.create(asignacion_data)
    
    def get_by_usuario_id(self, usuario_id: int) -> Optional[UsuarioAsignacion]:
        """
        Obtiene la asignación de un usuario
        
        Args:
            usuario_id (int): ID del usuario
            
        Returns:
            Optional[UsuarioAsignacion]: Asignación encontrada o None
        """
        try:
            return (
                self.db.query(UsuarioAsignacion)
                .filter(UsuarioAsignacion.usuario_id == usuario_id)
                .first()
            )
        except SQLAlchemyError as e:
            raise e
    
    def get_by_id(self, id_asignacion: int) -> Optional[UsuarioAsignacion]:
        """
        Obtiene una asignación por su ID
        
        Args:
            id_asignacion (int): ID de la asignación
            
        Returns:
            Optional[UsuarioAsignacion]: Asignación encontrada o None
        """
        try:
            return (
                self.db.query(UsuarioAsignacion)
                .filter(UsuarioAsignacion.id_asignacion == id_asignacion)
                .first()
            )
        except SQLAlchemyError as e:
            raise e
    
    def existe_asignacion_usuario(self, usuario_id: int) -> bool:
        """
        Verifica si un usuario ya tiene una asignación
        
        Args:
            usuario_id (int): ID del usuario
            
        Returns:
            bool: True si existe asignación, False si no
        """
        try:
            return (
                self.db.query(UsuarioAsignacion)
                .filter(UsuarioAsignacion.usuario_id == usuario_id)
                .first()
            ) is not None
        except SQLAlchemyError as e:
            raise e
    
    def get_usuarios_por_cliente(self, cliente_id: int):
        """
        Obtiene todos los usuarios asociados a un cliente
        
        Args:
            cliente_id (int): ID del cliente
            
        Returns:
            List[UsuarioAsignacion]: Lista de asignaciones
        """
        try:
            return (
                self.db.query(UsuarioAsignacion)
                .filter(
                    UsuarioAsignacion.cliente_id == cliente_id,
                    UsuarioAsignacion.tipo_asignacion == self.TIPO_CLIENTE
                )
                .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def delete(self, id_asignacion: int) -> bool:
        """
        Elimina una asignación (soft delete)
        
        Args:
            id_asignacion (int): ID de la asignación
            
        Returns:
            bool: True si se eliminó, False si no existe
        """
        try:
            asignacion = self.get_by_id(id_asignacion)
            if not asignacion:
                return False
            
            asignacion.estatus = 0
            self.db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def hard_delete(self, id_asignacion: int) -> bool:
        """
        Elimina físicamente una asignación
        
        Args:
            id_asignacion (int): ID de la asignación
            
        Returns:
            bool: True si se eliminó, False si no existe
        """
        try:
            asignacion = self.get_by_id(id_asignacion)
            if not asignacion:
                return False
            
            self.db.delete(asignacion)
            self.db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

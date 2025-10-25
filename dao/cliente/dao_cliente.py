"""
DAO (Data Access Object) para operaciones CRUD de Cliente
Maneja todas las interacciones con la base de datos para la entidad Cliente
Incluye validación de RFC único
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.cliente.cliente_model import Cliente
from schemas.cliente.cliente_create import ClienteCreate
from schemas.cliente.cliente_update import ClienteUpdate


class ClienteDAO:
    """
    Clase DAO para manejar operaciones CRUD de Cliente en la base de datos
    Utiliza SQLAlchemy ORM para las operaciones
    """

    __status_active__ = 1
    __status_inactive__ = 0
    
    def __init__(self, db_session: Session):
        """
        Inicializa el DAO con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy para operaciones de BD
        """
        self.db = db_session
    
    def create(self, cliente_data: ClienteCreate) -> Cliente:
        """
        Crea un nuevo cliente en la base de datos
        
        Args:
            cliente_data (ClienteCreate): Datos del cliente a crear
            
        Returns:
            Cliente: Objeto Cliente creado con ID asignado
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Crear objeto Cliente usando **data
            db_cliente = Cliente(**cliente_data.model_dump())
            
            # Agregar a la sesión y hacer commit
            self.db.add(db_cliente)
            self.db.commit()
            self.db.refresh(db_cliente)
            
            return db_cliente
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_by_id(self, id_cliente: int) -> Optional[Cliente]:
        """
        Obtiene un cliente por su ID
        
        Args:
            id_cliente (int): ID del cliente a buscar
            
        Returns:
            Optional[Cliente]: Cliente encontrado o None si no existe
        """
        try:
            return self.db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Cliente]:
        """
        Obtiene todos los clientes con paginación
        
        Args:
            skip (int): Número de registros a omitir
            limit (int): Número máximo de registros a retornar
            
        Returns:
            List[Cliente]: Lista de clientes
        """
        try:
            return (
                self.db.query(Cliente)
                .order_by(Cliente.id_cliente)
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def get_active(self, skip: int = 0, limit: int = 100) -> List[Cliente]:
        """
        Obtiene todos los clientes activos
        
        Args:
            skip (int): Número de registros a omitir
            limit (int): Número máximo de registros a retornar
            
        Returns:
            List[Cliente]: Lista de clientes activos
        """
        try:
            return (
                self.db.query(Cliente)
                .order_by(Cliente.id_cliente)
                .filter(Cliente.id_estatus == self.__status_active__)
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def get_by_rfc(self, rfc: str) -> Optional[Cliente]:
        """
        Obtiene un cliente por su RFC
        IMPORTANTE: Usado para validar RFC duplicado
        
        Args:
            rfc (str): RFC del cliente a buscar
            
        Returns:
            Optional[Cliente]: Cliente encontrado o None si no existe
        """
        try:
            if not rfc:
                return None
            return self.db.query(Cliente).filter(Cliente.rfc == rfc.upper().strip()).first()
        except SQLAlchemyError as e:
            raise e
    
    def exists_by_rfc(self, rfc: str, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica si existe un cliente con el RFC dado
        
        Args:
            rfc (str): RFC a verificar
            exclude_id (Optional[int]): ID a excluir de la búsqueda (para updates)
            
        Returns:
            bool: True si existe, False si no
        """
        try:
            if not rfc:
                return False
                
            rfc = rfc.upper().strip()
            query = self.db.query(Cliente).filter(Cliente.rfc == rfc)
            
            if exclude_id:
                query = query.filter(Cliente.id_cliente != exclude_id)
            
            return query.first() is not None
            
        except SQLAlchemyError as e:
            raise e
    
    def get_by_curp(self, curp: str) -> Optional[Cliente]:
        """
        Obtiene un cliente por su CURP
        
        Args:
            curp (str): CURP del cliente a buscar
            
        Returns:
            Optional[Cliente]: Cliente encontrado o None si no existe
        """
        try:
            if not curp:
                return None
            return self.db.query(Cliente).filter(Cliente.curp == curp.upper().strip()).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_by_correo_electronico(self, correo: str) -> Optional[Cliente]:
        """
        Obtiene un cliente por su correo electrónico
        
        Args:
            correo (str): Correo electrónico del cliente
            
        Returns:
            Optional[Cliente]: Cliente encontrado o None si no existe
        """
        try:
            if not correo:
                return None
            return self.db.query(Cliente).filter(Cliente.correo_electronico == correo.strip()).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_by_tipo_persona(self, tipo_persona: int, skip: int = 0, limit: int = 100) -> List[Cliente]:
        """
        Obtiene clientes filtrados por tipo de persona
        
        Args:
            tipo_persona (int): 1=Física, 2=Moral
            skip (int): Número de registros a omitir
            limit (int): Número máximo de registros
            
        Returns:
            List[Cliente]: Lista de clientes del tipo especificado
        """
        try:
            return (
                self.db.query(Cliente)
                .order_by(Cliente.id_cliente)
                .filter(Cliente.tipo_persona == tipo_persona)
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def update(self, id_cliente: int, cliente_data: ClienteUpdate) -> Optional[Cliente]:
        """
        Actualiza un cliente existente
        
        Args:
            id_cliente (int): ID del cliente a actualizar
            cliente_data (ClienteUpdate): Datos a actualizar
            
        Returns:
            Optional[Cliente]: Cliente actualizado o None si no existe
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar el cliente existente
            db_cliente = self.get_by_id(id_cliente)
            if not db_cliente:
                return None
            
            # Actualizar usando **data
            update_data = cliente_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_cliente, field, value)
            
            # Hacer commit de los cambios
            self.db.commit()
            self.db.refresh(db_cliente)
            
            return db_cliente
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def delete(self, id_cliente: int) -> bool:
        """
        Elimina un cliente (soft delete cambiando estatus)
        
        Args:
            id_cliente (int): ID del cliente a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False si no existe
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar el cliente existente
            db_cliente = self.get_by_id(id_cliente)
            if not db_cliente:
                return False
            
            # Soft delete: cambiar estatus a inactivo
            db_cliente.id_estatus = self.__status_inactive__
            
            # Hacer commit de los cambios
            self.db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def hard_delete(self, id_cliente: int) -> bool:
        """
        Elimina físicamente un cliente de la base de datos
        
        Args:
            id_cliente (int): ID del cliente a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False si no existe
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar el cliente existente
            db_cliente = self.get_by_id(id_cliente)
            if not db_cliente:
                return False
            
            # Eliminar físicamente
            self.db.delete(db_cliente)
            self.db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def search_by_nombre(self, nombre: str, skip: int = 0, limit: int = 100) -> List[Cliente]:
        """
        Busca clientes por nombre/razón social (búsqueda parcial)
        
        Args:
            nombre (str): Texto a buscar en nombre/razón social
            skip (int): Número de registros a omitir
            limit (int): Número máximo de registros
            
        Returns:
            List[Cliente]: Lista de clientes que coinciden con la búsqueda
        """
        try:
            return (
                self.db.query(Cliente)
                .filter(Cliente.nombre_razon_social.ilike(f"%{nombre}%"))
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            raise e

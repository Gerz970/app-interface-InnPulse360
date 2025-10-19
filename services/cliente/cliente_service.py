"""
Servicio de Cliente
Contiene la lógica de negocio para las operaciones relacionadas con clientes
Actúa como intermediario entre las rutas (API) y el DAO (acceso a datos)
Incluye validación de RFC único
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from dao.cliente.dao_cliente import ClienteDAO
from schemas.cliente.cliente_create import ClienteCreate
from schemas.cliente.cliente_update import ClienteUpdate
from schemas.cliente.cliente_response import ClienteResponse


class ClienteService:
    """
    Servicio que encapsula la lógica de negocio para operaciones de Cliente
    """
    
    def __init__(self, db_session: Session):
        """
        Inicializa el servicio con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy
        """
        self.dao = ClienteDAO(db_session)
    
    def crear_cliente(self, cliente_data: ClienteCreate) -> ClienteResponse:
        """
        Crea un nuevo cliente
        IMPORTANTE: Valida que el RFC no esté duplicado
        
        Args:
            cliente_data (ClienteCreate): Datos del cliente a crear
            
        Returns:
            ClienteResponse: Cliente creado
            
        Raises:
            ValueError: Si el RFC ya existe
            Exception: Si hay un error en la base de datos
        """
        try:
            # Validación de RFC único
            if cliente_data.rfc:
                if self.dao.exists_by_rfc(cliente_data.rfc):
                    raise ValueError(f"Ya existe un cliente registrado con el RFC '{cliente_data.rfc}'")
            
            # Crear cliente usando el DAO
            cliente_creado = self.dao.create(cliente_data)
            
            # Convertir a schema de respuesta
            return ClienteResponse.model_validate(cliente_creado)
            
        except ValueError as e:
            raise e
        except SQLAlchemyError as e:
            raise Exception(f"Error al crear cliente en la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al crear cliente: {str(e)}")
    
    def obtener_cliente_por_id(self, cliente_id: int) -> Optional[ClienteResponse]:
        """
        Obtiene un cliente por su ID
        
        Args:
            cliente_id (int): ID del cliente
            
        Returns:
            Optional[ClienteResponse]: Cliente encontrado o None
            
        Raises:
            Exception: Si hay un error en la base de datos
        """
        try:
            cliente = self.dao.get_by_id(cliente_id)
            
            if not cliente:
                return None
            
            return ClienteResponse.model_validate(cliente)
            
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener cliente de la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al obtener cliente: {str(e)}")
    
    def obtener_todos_los_clientes(self, skip: int = 0, limit: int = 100) -> List[ClienteResponse]:
        """
        Obtiene todos los clientes con paginación
        
        Args:
            skip (int): Número de registros a saltar
            limit (int): Número máximo de registros
            
        Returns:
            List[ClienteResponse]: Lista de clientes
            
        Raises:
            Exception: Si hay un error en la base de datos
        """
        try:
            clientes = self.dao.get_all(skip=skip, limit=limit)
            
            return [ClienteResponse.model_validate(cliente) for cliente in clientes]
            
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener clientes de la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al obtener clientes: {str(e)}")
    
    def obtener_clientes_activos(self, skip: int = 0, limit: int = 100) -> List[ClienteResponse]:
        """
        Obtiene todos los clientes activos con paginación
        
        Args:
            skip (int): Número de registros a saltar
            limit (int): Número máximo de registros
            
        Returns:
            List[ClienteResponse]: Lista de clientes activos
            
        Raises:
            Exception: Si hay un error en la base de datos
        """
        try:
            clientes = self.dao.get_active(skip=skip, limit=limit)
            
            return [ClienteResponse.model_validate(cliente) for cliente in clientes]
            
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener clientes activos de la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al obtener clientes activos: {str(e)}")
    
    def actualizar_cliente(self, cliente_id: int, cliente_data: ClienteUpdate) -> Optional[ClienteResponse]:
        """
        Actualiza un cliente existente
        IMPORTANTE: Valida que el RFC no esté duplicado si se actualiza
        
        Args:
            cliente_id (int): ID del cliente a actualizar
            cliente_data (ClienteUpdate): Datos a actualizar
            
        Returns:
            Optional[ClienteResponse]: Cliente actualizado o None si no existe
            
        Raises:
            ValueError: Si el RFC ya existe
            Exception: Si hay un error en la base de datos
        """
        try:
            # Verificar que el cliente existe
            cliente_existente = self.dao.get_by_id(cliente_id)
            if not cliente_existente:
                return None
            
            # Validación de RFC único si se está actualizando
            if cliente_data.rfc and cliente_data.rfc != cliente_existente.rfc:
                if self.dao.exists_by_rfc(cliente_data.rfc, exclude_id=cliente_id):
                    raise ValueError(f"Ya existe un cliente registrado con el RFC '{cliente_data.rfc}'")
            
            # Actualizar usando el DAO
            cliente_actualizado = self.dao.update(cliente_id, cliente_data)
            
            if not cliente_actualizado:
                return None
            
            return ClienteResponse.model_validate(cliente_actualizado)
            
        except ValueError as e:
            raise e
        except SQLAlchemyError as e:
            raise Exception(f"Error al actualizar cliente en la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al actualizar cliente: {str(e)}")
    
    def eliminar_cliente(self, cliente_id: int) -> bool:
        """
        Elimina un cliente (soft delete)
        
        Args:
            cliente_id (int): ID del cliente a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False si no existe
            
        Raises:
            Exception: Si hay un error en la base de datos
        """
        try:
            return self.dao.delete(cliente_id)
            
        except SQLAlchemyError as e:
            raise Exception(f"Error al eliminar cliente de la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al eliminar cliente: {str(e)}")
    
    def buscar_cliente_por_rfc(self, rfc: str) -> Optional[ClienteResponse]:
        """
        Busca un cliente por su RFC
        
        Args:
            rfc (str): RFC del cliente
            
        Returns:
            Optional[ClienteResponse]: Cliente encontrado o None
            
        Raises:
            Exception: Si hay un error en la base de datos
        """
        try:
            cliente = self.dao.get_by_rfc(rfc)
            
            if not cliente:
                return None
            
            return ClienteResponse.model_validate(cliente)
            
        except SQLAlchemyError as e:
            raise Exception(f"Error al buscar cliente por RFC: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al buscar cliente por RFC: {str(e)}")
    
    def buscar_clientes_por_nombre(self, nombre: str, skip: int = 0, limit: int = 100) -> List[ClienteResponse]:
        """
        Busca clientes por nombre/razón social
        
        Args:
            nombre (str): Texto a buscar
            skip (int): Número de registros a saltar
            limit (int): Número máximo de registros
            
        Returns:
            List[ClienteResponse]: Lista de clientes encontrados
            
        Raises:
            Exception: Si hay un error en la base de datos
        """
        try:
            clientes = self.dao.search_by_nombre(nombre, skip=skip, limit=limit)
            
            return [ClienteResponse.model_validate(cliente) for cliente in clientes]
            
        except SQLAlchemyError as e:
            raise Exception(f"Error al buscar clientes por nombre: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al buscar clientes por nombre: {str(e)}")
    
    def obtener_clientes_por_tipo_persona(self, tipo_persona: int, skip: int = 0, limit: int = 100) -> List[ClienteResponse]:
        """
        Obtiene clientes filtrados por tipo de persona
        
        Args:
            tipo_persona (int): 1=Física, 2=Moral
            skip (int): Número de registros a saltar
            limit (int): Número máximo de registros
            
        Returns:
            List[ClienteResponse]: Lista de clientes
            
        Raises:
            Exception: Si hay un error en la base de datos
        """
        try:
            clientes = self.dao.get_by_tipo_persona(tipo_persona, skip=skip, limit=limit)
            
            return [ClienteResponse.model_validate(cliente) for cliente in clientes]
            
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener clientes por tipo de persona: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al obtener clientes por tipo de persona: {str(e)}")
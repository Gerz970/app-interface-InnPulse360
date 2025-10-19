"""
DAO (Data Access Object) para operaciones de asociación Módulo-Rol
Maneja las relaciones entre módulos y roles
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from models.seguridad.modulos_model import modulo_rol
from models.seguridad.modulos_model import Modulos
from models.seguridad.roles_model import Roles


class ModuloRolDAO:
    """
    Clase DAO para manejar las asociaciones entre módulos y roles
    """

    def __init__(self, db_session: Session):
        """
        Inicializa el DAO con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy para operaciones de BD
        """
        self.db = db_session
    
    def asignar_modulo_a_rol(self, modulo_id: int, rol_id: int) -> bool:
        """
        Asigna un módulo a un rol
        
        Args:
            modulo_id (int): ID del módulo
            rol_id (int): ID del rol
            
        Returns:
            bool: True si se asignó correctamente
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Verificar que el módulo y rol existen
            modulo = self.db.query(Modulos).filter(Modulos.id_modulo == modulo_id).first()
            rol = self.db.query(Roles).filter(Roles.id_rol == rol_id).first()
            
            if not modulo or not rol:
                return False
            
            # Verificar si ya existe la asociación
            if self.existe_asociacion(modulo_id, rol_id):
                return True  # Ya existe, no es error
            
            # Crear la asociación usando SQL directo para evitar problemas con la tabla intermedia
            query = text("""
                INSERT INTO SEGURIDAD.Tb_modulo_rol (modulo_id, rol_id)
                VALUES (:modulo_id, :rol_id)
            """)
            
            self.db.execute(query, {"modulo_id": modulo_id, "rol_id": rol_id})
            self.db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def desasignar_modulo_de_rol(self, modulo_id: int, rol_id: int) -> bool:
        """
        Desasigna un módulo de un rol
        
        Args:
            modulo_id (int): ID del módulo
            rol_id (int): ID del rol
            
        Returns:
            bool: True si se desasignó correctamente
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Eliminar la asociación usando SQL directo
            query = text("""
                DELETE FROM SEGURIDAD.Tb_modulo_rol 
                WHERE modulo_id = :modulo_id AND rol_id = :rol_id
            """)
            
            result = self.db.execute(query, {"modulo_id": modulo_id, "rol_id": rol_id})
            self.db.commit()
            
            return result.rowcount > 0
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def asignar_multiples_modulos_a_rol(self, rol_id: int, modulos_ids: List[int]) -> bool:
        """
        Asigna múltiples módulos a un rol
        
        Args:
            rol_id (int): ID del rol
            modulos_ids (List[int]): Lista de IDs de módulos
            
        Returns:
            bool: True si se asignaron correctamente
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Verificar que el rol existe
            rol = self.db.query(Roles).filter(Roles.id_rol == rol_id).first()
            if not rol:
                return False
            
            # Verificar que todos los módulos existen
            modulos_existentes = self.db.query(Modulos).filter(
                Modulos.id_modulo.in_(modulos_ids)
            ).all()
            
            if len(modulos_existentes) != len(modulos_ids):
                return False
            
            # Asignar cada módulo al rol
            for modulo_id in modulos_ids:
                if not self.existe_asociacion(modulo_id, rol_id):
                    self.asignar_modulo_a_rol(modulo_id, rol_id)
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def desasignar_todos_los_modulos_de_rol(self, rol_id: int) -> bool:
        """
        Desasigna todos los módulos de un rol
        
        Args:
            rol_id (int): ID del rol
            
        Returns:
            bool: True si se desasignaron correctamente
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Eliminar todas las asociaciones del rol
            query = text("""
                DELETE FROM SEGURIDAD.Tb_modulo_rol 
                WHERE rol_id = :rol_id
            """)
            
            result = self.db.execute(query, {"rol_id": rol_id})
            self.db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def existe_asociacion(self, modulo_id: int, rol_id: int) -> bool:
        """
        Verifica si existe una asociación entre un módulo y un rol
        
        Args:
            modulo_id (int): ID del módulo
            rol_id (int): ID del rol
            
        Returns:
            bool: True si existe la asociación
        """
        try:
            query = text("""
                SELECT COUNT(*) as count
                FROM SEGURIDAD.Tb_modulo_rol 
                WHERE modulo_id = :modulo_id AND rol_id = :rol_id
            """)
            
            result = self.db.execute(query, {"modulo_id": modulo_id, "rol_id": rol_id})
            count = result.fetchone()[0]
            
            return count > 0
            
        except SQLAlchemyError as e:
            raise e
    
    def get_modulos_por_rol(self, rol_id: int) -> List[Modulos]:
        """
        Obtiene todos los módulos asignados a un rol
        
        Args:
            rol_id (int): ID del rol
            
        Returns:
            List[Modulos]: Lista de módulos asignados al rol
        """
        try:
            return (
                self.db.query(Modulos)
                .join(modulo_rol, Modulos.id_modulo == modulo_rol.c.modulo_id)
                .filter(modulo_rol.c.rol_id == rol_id)
                .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def get_roles_por_modulo(self, modulo_id: int) -> List[Roles]:
        """
        Obtiene todos los roles asignados a un módulo
        
        Args:
            modulo_id (int): ID del módulo
            
        Returns:
            List[Roles]: Lista de roles asignados al módulo
        """
        try:
            return (
                self.db.query(Roles)
                .join(modulo_rol, Roles.id_rol == modulo_rol.c.rol_id)
                .filter(modulo_rol.c.modulo_id == modulo_id)
                .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def get_asociaciones_por_rol(self, rol_id: int) -> List[dict]:
        """
        Obtiene las asociaciones de módulos con un rol específico
        
        Args:
            rol_id (int): ID del rol
            
        Returns:
            List[dict]: Lista de asociaciones con información del módulo
        """
        try:
            query = text("""
                SELECT 
                    mr.modulo_id,
                    mr.rol_id,
                    m.nombre as modulo_nombre,
                    r.rol as rol_nombre
                FROM SEGURIDAD.Tb_modulo_rol mr
                INNER JOIN SEGURIDAD.Tb_Modulos m ON mr.modulo_id = m.id_modulo
                INNER JOIN SEGURIDAD.Tb_rol r ON mr.rol_id = r.id_rol
                WHERE mr.rol_id = :rol_id
            """)
            
            result = self.db.execute(query, {"rol_id": rol_id})
            return [dict(row) for row in result]
            
        except SQLAlchemyError as e:
            raise e

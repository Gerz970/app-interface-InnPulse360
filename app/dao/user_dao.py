"""
Módulo Data Access Object para Usuario.

Este módulo proporciona la capa de acceso a datos para entidades de Usuario,
manejando todas las operaciones de base de datos de manera centralizada.
"""

from sqlalchemy.orm import Session

from app.models import User as UserModel
from app.schemas import UserCreate


class UserDAO:
    """
    Objeto de Acceso a Datos para operaciones de Usuario.

    Proporciona operaciones CRUD para entidades de Usuario usando SQLAlchemy.
    Cada instancia está ligada a una sesión específica de base de datos.

    Atributos:
        db (Session): Sesión de base de datos SQLAlchemy
    """

    def __init__(self, db: Session):
        """
        Inicializar UserDAO con una sesión de base de datos.

        Args:
            db (Session): Sesión de base de datos SQLAlchemy
        """
        self.db = db

    def get_user(self, user_id: int):
        """
        Obtener un usuario por ID.

        Args:
            user_id (int): El identificador único del usuario

        Returns:
            UserModel or None: El usuario si se encuentra, None en caso contrario
        """
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_users(self, skip: int = 0, limit: int = 100):
        """
        Obtener una lista de usuarios con paginación.

        Args:
            skip (int): Número de registros a saltar (por defecto: 0)
            limit (int): Número máximo de registros a retornar (por defecto: 100)

        Returns:
            list[UserModel]: Lista de registros de usuario
        """
        return self.db.query(UserModel).offset(skip).limit(limit).all()

    def create_user(self, user: UserCreate):
        """
        Crear un nuevo usuario en la base de datos.

        Args:
            user (UserCreate): Datos del usuario para creación

        Returns:
            UserModel: El usuario creado con ID generado
        """
        db_user = UserModel(name=user.name, email=user.email)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user_id: int, user: UserCreate):
        """
        Actualizar un usuario existente.

        Args:
            user_id (int): ID del usuario a actualizar
            user (UserCreate): Datos actualizados del usuario

        Returns:
            UserModel or None: Usuario actualizado si se encuentra, None en caso contrario
        """
        db_user = self.get_user(user_id)
        if db_user:
            db_user.name = user.name
            db_user.email = user.email
            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int):
        """
        Eliminar un usuario de la base de datos.

        Args:
            user_id (int): ID del usuario a eliminar

        Returns:
            UserModel or None: Usuario eliminado si se encuentra, None en caso contrario
        """
        db_user = self.get_user(user_id)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
        return db_user
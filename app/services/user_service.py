"""
Módulo de servicio de lógica de negocio para Usuario.

Este módulo contiene la capa de lógica de negocio para operaciones de Usuario,
proporcionando validación, transformación y coordinación entre
capas DAO y API.
"""

from sqlalchemy.orm import Session

from app.dao import UserDAO
from app.schemas import User, UserCreate


class UserService:
    """
    Clase de servicio para operaciones de negocio de usuario.

    Maneja lógica de negocio, validación y coordina entre
    capas de acceso a datos y presentación.

    Atributos:
        dao (UserDAO): Objeto de acceso a datos para operaciones de usuario
    """

    def __init__(self, db: Session):
        """
        Inicializar UserService con sesión de base de datos.

        Args:
            db (Session): Sesión de base de datos SQLAlchemy
        """
        self.dao = UserDAO(db)

    def get_user(self, user_id: int) -> User | None:
        """
        Obtener un usuario por ID con conversión de esquema.

        Args:
            user_id (int): El identificador único del usuario

        Returns:
            User or None: Esquema Pydantic User si se encuentra, None en caso contrario
        """
        user = self.dao.get_user(user_id)
        return User.from_orm(user) if user else None

    def get_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """
        Obtener una lista paginada de usuarios.

        Args:
            skip (int): Número de registros a saltar (por defecto: 0)
            limit (int): Número máximo de registros a retornar (por defecto: 100)

        Returns:
            list[User]: Lista de esquemas User
        """
        users = self.dao.get_users(skip, limit)
        return [User.from_orm(user) for user in users]

    def create_user(self, user: UserCreate) -> User:
        """
        Crear un nuevo usuario con validación de negocio.

        Realiza validaciones como verificar emails duplicados
        antes de crear el usuario.

        Args:
            user (UserCreate): Datos de creación del usuario

        Returns:
            User: Esquema del usuario creado

        Raises:
            ValueError: Si el email ya existe
        """
        # Lógica de negocio: verificar si el email ya existe
        from app.models import User as UserModel
        existing = self.dao.db.query(UserModel).filter(UserModel.email == user.email).first()
        if existing:
            raise ValueError("Email already exists")
        db_user = self.dao.create_user(user)
        return User.from_orm(db_user)

    def update_user(self, user_id: int, user: UserCreate) -> User | None:
        """
        Actualizar un usuario existente.

        Args:
            user_id (int): ID del usuario a actualizar
            user (UserCreate): Datos actualizados del usuario

        Returns:
            User or None: Esquema del usuario actualizado si se encuentra, None en caso contrario
        """
        db_user = self.dao.update_user(user_id, user)
        return User.from_orm(db_user) if db_user else None

    def delete_user(self, user_id: int) -> User | None:
        """
        Eliminar un usuario.

        Args:
            user_id (int): ID del usuario a eliminar

        Returns:
            User or None: Esquema del usuario eliminado si se encuentra, None en caso contrario
        """
        db_user = self.dao.delete_user(user_id)
        return User.from_orm(db_user) if db_user else None
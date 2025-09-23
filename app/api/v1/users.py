"""
Módulo de endpoints de API para Usuario.

Este módulo define rutas FastAPI para operaciones de gestión de usuarios,
proporcionando endpoints RESTful para operaciones CRUD en usuarios.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core import get_db
from app.schemas import User, UserCreate
from app.services import UserService

router = APIRouter()


@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo usuario.

    Valida los datos del usuario y crea un nuevo registro de usuario en la base de datos.

    Args:
        user (UserCreate): Datos de creación del usuario
        db (Session): Dependencia de sesión de base de datos

    Returns:
        User: Datos del usuario creado

    Raises:
        HTTPException: 400 si el email ya existe o falla la validación
    """
    service = UserService(db)
    try:
        return service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Obtener un usuario específico por ID.

    Args:
        user_id (int): El identificador único del usuario
        db (Session): Dependencia de sesión de base de datos

    Returns:
        User: Datos del usuario

    Raises:
        HTTPException: 404 si el usuario no se encuentra
    """
    service = UserService(db)
    user = service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtener una lista paginada de usuarios.

    Args:
        skip (int): Número de registros a saltar (por defecto: 0)
        limit (int): Número máximo de registros a retornar (por defecto: 100)
        db (Session): Dependencia de sesión de base de datos

    Returns:
        list[User]: Lista de usuarios
    """
    service = UserService(db)
    return service.get_users(skip, limit)


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    """
    Actualizar un usuario existente.

    Args:
        user_id (int): ID del usuario a actualizar
        user (UserCreate): Datos actualizados del usuario
        db (Session): Dependencia de sesión de base de datos

    Returns:
        User: Datos del usuario actualizado

    Raises:
        HTTPException: 404 si el usuario no se encuentra
    """
    service = UserService(db)
    updated_user = service.update_user(user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/{user_id}", response_model=User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un usuario.

    Args:
        user_id (int): ID del usuario a eliminar
        db (Session): Dependencia de sesión de base de datos

    Returns:
        User: Datos del usuario eliminado

    Raises:
        HTTPException: 404 si el usuario no se encuentra
    """
    service = UserService(db)
    deleted_user = service.delete_user(user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user
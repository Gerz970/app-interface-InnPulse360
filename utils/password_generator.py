"""
Utilidad para generar contraseñas temporales seguras
"""

import secrets
import string
from typing import Tuple


def generar_password_temporal(longitud: int = 12) -> str:
    """
    Genera una contraseña temporal segura
    
    La contraseña incluye:
    - Letras mayúsculas
    - Letras minúsculas
    - Números
    - Al menos un carácter de cada tipo
    
    Args:
        longitud (int): Longitud de la contraseña (mínimo 8, por defecto 12)
        
    Returns:
        str: Contraseña temporal generada
        
    Example:
        >>> password = generar_password_temporal()
        >>> len(password)
        12
        >>> password = generar_password_temporal(16)
        >>> len(password)
        16
    """
    if longitud < 8:
        longitud = 8
    
    # Definir caracteres permitidos
    mayusculas = string.ascii_uppercase
    minusculas = string.ascii_lowercase
    numeros = string.digits
    
    # Asegurar al menos un carácter de cada tipo
    password = [
        secrets.choice(mayusculas),
        secrets.choice(minusculas),
        secrets.choice(numeros),
    ]
    
    # Completar el resto de la longitud con caracteres aleatorios
    todos_caracteres = mayusculas + minusculas + numeros
    password.extend(secrets.choice(todos_caracteres) for _ in range(longitud - 3))
    
    # Mezclar los caracteres
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)


def generar_password_compleja(longitud: int = 16) -> str:
    """
    Genera una contraseña compleja con símbolos especiales
    
    Args:
        longitud (int): Longitud de la contraseña (mínimo 12, por defecto 16)
        
    Returns:
        str: Contraseña compleja generada
    """
    if longitud < 12:
        longitud = 12
    
    mayusculas = string.ascii_uppercase
    minusculas = string.ascii_lowercase
    numeros = string.digits
    simbolos = "!@#$%&*-_"
    
    # Asegurar al menos un carácter de cada tipo
    password = [
        secrets.choice(mayusculas),
        secrets.choice(minusculas),
        secrets.choice(numeros),
        secrets.choice(simbolos),
    ]
    
    # Completar el resto
    todos_caracteres = mayusculas + minusculas + numeros + simbolos
    password.extend(secrets.choice(todos_caracteres) for _ in range(longitud - 4))
    
    # Mezclar
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)


def validar_fortaleza_password(password: str) -> Tuple[bool, str]:
    """
    Valida la fortaleza de una contraseña
    
    Requisitos:
    - Mínimo 6 caracteres
    - Al menos una mayúscula
    - Al menos una minúscula
    - Al menos un número
    
    Args:
        password (str): Contraseña a validar
        
    Returns:
        Tuple[bool, str]: (es_valida, mensaje)
        
    Example:
        >>> validar_fortaleza_password("abc")
        (False, "La contraseña debe tener al menos 6 caracteres")
        >>> validar_fortaleza_password("Password123")
        (True, "Contraseña válida")
    """
    if len(password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres"
    
    tiene_mayuscula = any(c.isupper() for c in password)
    tiene_minuscula = any(c.islower() for c in password)
    tiene_numero = any(c.isdigit() for c in password)
    
    if not tiene_mayuscula:
        return False, "La contraseña debe contener al menos una letra mayúscula"
    
    if not tiene_minuscula:
        return False, "La contraseña debe contener al menos una letra minúscula"
    
    if not tiene_numero:
        return False, "La contraseña debe contener al menos un número"
    
    return True, "Contraseña válida"

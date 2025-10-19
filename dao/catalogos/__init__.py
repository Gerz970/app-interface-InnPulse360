"""
DAO para módulo de catálogos
Contiene DAOs para datos maestros y catálogos del sistema
"""

from .dao_estado import EstadoDAO
from .dao_pais import PaisDAO

__all__ = ["EstadoDAO", "PaisDAO"]

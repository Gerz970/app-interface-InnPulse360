"""
Schemas Pydantic para gestión de tokens de dispositivos FCM
"""

from pydantic import BaseModel, Field
from typing import Optional


class DeviceTokenRequest(BaseModel):
    """
    Schema para registrar un token de dispositivo
    """
    device_token: str = Field(
        ...,
        description="Token FCM del dispositivo",
        example="dK3jH9sL2mN8pQ5rT7vW1xY4zA6bC8dE0fG2hI4jK6lM8nO0pQ2rS4tU6vW8xY0zA2bC4dE6fG8hI0jK2lM4nO6pQ8rS0tU2vW4xY6zA8bC0dE2fG4hI6jK8lM0nO2pQ4rS6tU8vW0xY2zA4bC6dE8fG0hI2jK4lM6nO8pQ0rS2tU4vW6xY8zA0bC2dE4fG6hI8jK0lM2nO4pQ6rS8tU0vW2xY4zA6bC8dE0"
    )
    plataforma: str = Field(
        ...,
        description="Plataforma del dispositivo",
        example="android",
        pattern="^(android|ios)$"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "device_token": "dK3jH9sL2mN8pQ5rT7vW1xY4zA6bC8dE0fG2hI4jK6lM8nO0pQ2rS4tU6vW8xY0zA2bC4dE6fG8hI0jK2lM4nO6pQ8rS0tU2vW4xY6zA8bC0dE2fG4hI6jK8lM0nO2pQ4rS6tU8vW0xY2zA4bC6dE8fG0hI2jK4lM6nO8pQ0rS2tU4vW6xY8zA0bC2dE4fG6hI8jK0lM2nO4pQ6rS8tU0vW2xY4zA6bC8dE0",
                "plataforma": "android"
            }
        }


class DeviceTokenResponse(BaseModel):
    """
    Schema para respuesta al registrar un token
    """
    success: bool = Field(
        ...,
        description="Indica si la operación fue exitosa"
    )
    message: str = Field(
        ...,
        description="Mensaje descriptivo del resultado"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Token registrado exitosamente en la base de datos"
            }
        }


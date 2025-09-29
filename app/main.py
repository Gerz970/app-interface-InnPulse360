from fastapi import FastAPI
from core.config import Settings
from api.v1 import api_router
from core.database_connection import db_connection

# Crear instancia de settings
settings = Settings()


# Crear instancia de FastAPI
app = FastAPI(title="InnPulse360 API", version="1.0.0")

# Incluir el router de la API v1
app.include_router(api_router, prefix=settings.api_version)

# Endpoint de bienvenida
@app.get("/")
def read_root():
    return {"message": "Bienvenido a InnPulse360 API"}

@app.get("/test-db")
def test_db():
    """devuelve verdadero si la conexión a la base de datos es exitosa
    """
    return db_connection.test_connection()


# Iniciar el servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)
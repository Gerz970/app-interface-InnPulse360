from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from core.config import Settings
from api.v1 import api_router
from api.v1.routes_websocket import register_websocket_endpoint
from core.database_connection import db_connection

# Crear instancia de settings
settings = Settings()


# Crear instancia de FastAPI
app = FastAPI(title="InnPulse360 API", version="1.0.0")

# CORS
# Lista de orígenes permitidos
origins = ["*"] # Todos los orígenes permitidos

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # dominios permitidos * = todos
    allow_credentials=True,         # si vas a usar cookies o auth * = todos
    allow_methods=["*"],            # GET, POST, PUT... "*" = todos
    allow_headers=["*"],            # encabezados permitidos * = todos
)

# Incluir el router de la API v1
app.include_router(api_router, prefix=settings.api_version)

# Registrar endpoint WebSocket
register_websocket_endpoint(app)

# Endpoint de bienvenida
@app.get("/")
def read_root():
    return {"message": "Bienvenido a InnPulse360 API"}


"""
@app.get("/test-db")
def test_db():
    #devuelve verdadero si la conexión a la base de datos es exitosa
    
    return db_connection.test_connection()
"""


# Iniciar el servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)
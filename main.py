import uvicorn

from app.api import app
from app.core import engine
from app.models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
from sqlalchemy.orm import declarative_base

# Base centralizada para todos los modelos del proyecto
# Este es el único punto donde se define declarative_base()
Base = declarative_base()
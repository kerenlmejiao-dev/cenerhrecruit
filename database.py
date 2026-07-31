"""
database.py - Configuración de base de datos compartida

Extraído de api.py para que otros módulos (auth_users.py, y en el
futuro los routers de portal) puedan importar el engine/sesión sin
crear un import circular con api.py.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cenerh_recruit.db")
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

class Parametres:
    PROJECT_NAME: str = "api-noabag"
    PROJECT_VERSION: str = "0.0.0"
    DATABASE_URL: str = "mysql+pymysql://444105:emore291961@mysql-proddebugger.alwaysdata.net:3306/proddebugger_noagab"
    #DATABASE_URL: str = "mysql+pymysql://root@localhost:3306/bdd-noa"

parametres = Parametres()

engine = create_engine(
    parametres.DATABASE_URL,
    pool_size=5,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=120,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

try:
    with engine.connect() as connection:
        print("Connexion à la base de donnée établie avec succès")
except SQLAlchemyError as e:
    print("Erreur de connexion à la base de donnée: ", str(e))


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


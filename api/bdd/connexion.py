

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class Parametres:
    PROJECT_NAME: str = "api-noabag"
    PROJECT_VERSION: str = "0.0.0"
    DATABASE_URL: str = "mysql+pymysql://442597:emore291961@mysql-test-projet.alwaysdata.net:3306/test-projet_noa"

parametres = Parametres()

engine = create_engine(Parametres.DATABASE_URL)

try:
    with engine.connect() as connection:
        print("Connexion à la base de donnée établie avec succès")
except SQLAlchemyError as e:
    print("Erreur de connexion à la base de donnée: ", str(e))


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


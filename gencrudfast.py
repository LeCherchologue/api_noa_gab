import os
import sys
from textwrap import dedent


def ensure_package(path):
    if not os.path.exists(path):
        os.makedirs(path)
    init_file = os.path.join(path, "__init__.py")
    if not os.path.exists(init_file):
        with open(init_file, "w") as f:
            f.write("")


def gen_crud(name, *fields):
    name = name.capitalize()
    fields_str = "\n".join([f"{f} = Column(String(255))" for f in fields])
    fields_schema = "\n".join([f"{f} : str" for f in fields])

    # --- Models ---
    model = dedent(f"""
    from sqlalchemy import Column, Integer, String, func, DateTime, Boolean, ForeignKey,Date
    from sqlalchemy.orm import relationship
    from ..bdd.connexion import Base

    class {name}(Base):
        __tablename__ = "{name.lower()}"
        id = Column(Integer, primary_key=True, index=True, autoincrement=True)
        {fields_str}
        created_at = Column(DateTime, default=func.now(), nullable=False)
        updated_at = Column(DateTime, default=func.now(), nullable=False)
    """)

    # --- Schemas ---
    schema = dedent(f"""
    from pydantic import BaseModel, EmailStr
    from typing import Optional
    from datetime import datetime

    class {name}Schema(BaseModel):

        {fields_schema}
    """)

    # --- Routes ---
    router = dedent(f""""
    from sqlalchemy.orm import Session
    from fastapi import APIRouter, Depends,Form, UploadFile,File
    from api.bdd.connexion import SessionLocal
    from api.schema.{name}Schema import {name}Schema
    from api.controller import {name}Controller

    router = APIRouter()

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    #--------------route {name}--------------------#

    @router.get("/{name.lower()}" , tags=["{name.lower()}"], response_model=list[{name}Schema])
    async def get_{name.lower()}():
        return {name}Controller.get_all_{name.lower()}(db=SessionLocal())

    @router.post("/{name.lower()}", tags=["{name.lower()}"])
    async def create_{name.lower()}({name.lower()}: {name}Schema):
        db=SessionLocal()
        return {name}Controller.create_{name.lower()}(db=db, {name.lower()}={name.lower()})

    @router.put("/{name.lower()}/id", tags=["{name.lower()}"])
    async def update_{name.lower()}(id: int, {name.lower()}: {name}Schema):
        db=SessionLocal()
        return {name}Controller.update_{name.lower()}(db=db, {name.lower()}={name.lower()}, {name.lower()}_id=id)

    @router.delete("/{name.lower()}/id", tags=["{name.lower()}"])
    async def delete_{name.lower()}(id: int):
        db=SessionLocal()
        return {name}Controller.delete_{name.lower()}(db=db, id=id)

    """)

    # --- Controllers ---

    controller = dedent(f""" 
    from sqlalchemy.orm import Session
    from fastapi import UploadFile, HTTPException
    from ..model.{name}Model import {name}
    from ..model import {name}Model
    from ..schema import {name}Schema

    #------------------------------------requetes crud {name.lower()}--------------------------------#

    def get_all_{name.lower()}(db: Session):
        return db.query({name}Model.{name}).all()

    def create_{name.lower()}(db: Session, {name.lower()}: {name}Schema):

        new_{name.lower()} = {name}(**{name.lower()}.dict())

        db.add(new_{name.lower()})
        db.commit()
        db.refresh(new_{name.lower()})

        return {{
            "message": "{name.lower()} cree",
            "detail": "success",
            "{name.lower()}": new_{name.lower()}
        }}

    def update_{name.lower()}(db: Session, {name.lower()}_id: int, {name.lower()}: {name}Schema):

        db_{name.lower()} = db.query({name}).filter({name}.id == {name.lower()}_id).first()
        if not db_{name.lower()}:
            raise HTTPException(status_code=404, detail="{name} non trouvé")

        for key, value in {name.lower()}.dict().items():
            setattr(db_{name.lower()}, key, value)

        db.commit()
        db.refresh(db_{name.lower()})

        return {{
            "message": "{name.lower()} mis à jour avec succès",
            "detail": "success",
            "{name.lower()}": db_{name.lower()}
        }}

    def delete_{name.lower()}(db: Session, id: int):
        del_{name.lower()} = db.query({name}).filter({name}.id == id).first()
        if not del_{name.lower()}:
            raise HTTPException(status_code=404, detail="{name} non trouvé")
        db.delete(del_{name.lower()})
        db.commit()
    """)

    # --- Écriture des fichiers ---
    os.makedirs("api/model", exist_ok=True)
    os.makedirs("api/schema", exist_ok=True)
    os.makedirs("api/router", exist_ok=True)
    os.makedirs("api/controller", exist_ok=True)

    ensure_package("api/model")
    with open(f"api/model/{name}Model.py", "w") as f:
        f.write(model)

    ensure_package("api/schema")
    with open(f"api/schema/{name}Schema.py", "w") as f:
        f.write(schema)

    ensure_package("api/router")
    with open(f"api/router/{name}Router.py", "w") as f:
        f.write(router)

    ensure_package("api/controller")
    with open(f"api/controller/{name}Controller.py", "w") as f:
        f.write(controller)

    print(f"✅ CRUD généré pour  {name} ({', '.join(fields)}) avec succes !!!")


def gen_main(firstTable: str):
    firstTable = firstTable.capitalize()

    main = dedent(f"""  
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from api.router import {firstTable}Router
    from api.bdd.connexion import Base, engine

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["POST", "GET", "PUT", "DELETE"],
        allow_headers=["*"],
    )

    Base.metadata.create_all(bind=engine)

    app.include_router({firstTable}Router.router, prefix="/api")

    @app.get("/")
    async def main():
        return {{
            "message": "API demarre",
        }}

    """)

    # --- Écriture du fichier ---
    with open(f"main.py", "w") as f:
        f.write(main)

    print("le fichier main.py, success ")


def gen_bdd(name_bdd, name_projet):
    bdd = dedent(f"""

    from sqlalchemy import create_engine
    from sqlalchemy.exc import SQLAlchemyError
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker

    class Parametres:
    PROJECT_NAME: str = {name_projet}
    PROJECT_VERSION: str = "0.0.0"
    DATABASE_URL: str = "mysql+pymysql://root@localhost:3306/{name_bdd}"

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

    """)

    os.makedirs("api/bdd", exist_ok=True)

    ensure_package("api/bdd")
    with open(f"api/bdd/connexion.py", "w") as f:
        f.write(bdd)

    print("Base de donne cree avec success")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python cli.py make:crud NomModel champ1 champ2 ...")
    else:
        cmd = sys.argv[1]
        if cmd == "make:crud":
            gen_crud(*sys.argv[2:])

        if cmd == "make:main":
            gen_main(sys.argv[2])

        if cmd == "make:bdd":
            gen_bdd(*sys.argv[2:])

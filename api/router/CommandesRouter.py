from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends,Form, UploadFile,File
from api.bdd.connexion import SessionLocal
from api.schema.CommandesSchema import CommandesSchema
from api.controller import CommandesController

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#--------------route Commandes--------------------#

@router.get("/commandes" , tags=["commandes"], response_model=list[CommandesSchema])
async def get_commandes():
    return CommandesController.get_all_commandes(db=SessionLocal())

@router.post("/commandes", tags=["commandes"])
async def create_commandes(commandes: CommandesSchema):
    db=SessionLocal()
    return CommandesController.create_commandes(db=db, commandes=commandes)

@router.put("/commandes/{id}", tags=["commandes"])
async def update_commandes(id: int, commandes: CommandesSchema):
    db=SessionLocal()
    return CommandesController.update_commandes(db=db, commandes=commandes, commandes_id=id)

@router.delete("/commandes/{id}", tags=["commandes"])
async def delete_commandes(id: int):
    db=SessionLocal()
    return CommandesController.delete_commandes(db=db, id=id)


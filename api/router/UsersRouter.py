from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends,Form, UploadFile,File
from api.bdd.connexion import SessionLocal
from api.schema.UsersSchema import UsersSchema, UserOut
from api.controller import UsersController

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#--------------route authentification--------------------#
@router.post("/login", tags=["authentification"])
async def login(user: UserOut):
    db=SessionLocal()
    return UsersController.authenticate_user(db=db, user=user)

#--------------route Users--------------------#

@router.get("/users" , tags=["users"], response_model=list[UsersSchema])
async def get_users():
    return UsersController.get_all_users(db=SessionLocal())

@router.post("/users", tags=["users"])
async def create_users(users: UsersSchema):
    db=SessionLocal()
    return UsersController.create_users(db=db, users=users)

@router.put("/users/{id}", tags=["users"])
async def update_users(id: int, users: UsersSchema):
    db=SessionLocal()
    return UsersController.update_users(db=db, users=users, users_id=id)

@router.delete("/users/{id}", tags=["users"])
async def delete_users(id: int):
    db=SessionLocal()
    return UsersController.delete_users(db=db, id=id)


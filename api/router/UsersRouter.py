from typing import Generator, Annotated

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends,Form, UploadFile,File
from fastapi.responses import Response
from api.bdd.connexion import SessionLocal
from api.bdd.security import  get_current_user
from api.controller.UsersController import authenticate_user
from api.schema.UsersSchema import UsersSchema, UserOut,UserAuth
from api.controller import UsersController
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




#--------------route authentification--------------------#
@router.post("/login", tags=["authentification"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return authenticate_user(db, form_data)

#--------------route Users--------------------#

@router.get("/users" , tags=["users"], response_model=list[UserOut])
async def get_users(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    return UsersController.get_all_users(db=db)

@router.post("/users", tags=["users"])
async def create_users(users: UsersSchema, db: Session = Depends(get_db)):
    return UsersController.create_users(db=db, users=users)

@router.put("/users/{id}", tags=["users"])
async def update_users(id: int, users: UserOut, db: Session = Depends(get_db)):
    return UsersController.update_users(db=db, users=users, users_id=id)

@router.delete("/users/{id}", tags=["users"])
async def delete_users(id: int, db: Session = Depends(get_db)):
    return UsersController.delete_users(db=db, id=id)


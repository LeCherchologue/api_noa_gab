
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UsersSchema(BaseModel):

    #id: int
    nom : str
    prenom : str
    email : str
    tel : str
    adresse : str
    profil : str
    password : str

class UserOut(BaseModel):

    id: int
    nom: str
    prenom: str
    email: str
    tel: str
    adresse: str
    profil: str

class UserAuth(BaseModel):
    email: str
    password: str

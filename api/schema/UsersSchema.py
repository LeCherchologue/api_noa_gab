
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UsersSchema(BaseModel):

    id: int
    nom : str
    prenom : str
    email : str
    tel : str
    adresse : str
    profil : str
    password : str

class UserAuthentication(BaseModel):
    email: str
    password: str

from pydantic import BaseModel, EmailStr, Field
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
    password : str = Field(..., max_length=72)

class UserOut(BaseModel):

    id: int
    nom: str
    prenom: str
    email: str
    tel: str
    adresse: str
    profil: str

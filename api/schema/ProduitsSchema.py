from fastapi import Depends, UploadFile, File, Form, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ProduitsSchema(BaseModel):

    id: int
    nom : str
    prix : str
    categorie : str
    description : str
    statut : str
    quantite : str
    images : str

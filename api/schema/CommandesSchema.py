
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class CommandesSchema(BaseModel):

    quantite : int
    total : int
    produit_id : int
    user_id : int

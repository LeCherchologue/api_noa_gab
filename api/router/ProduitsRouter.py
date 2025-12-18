from typing import Generator

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Form, UploadFile, File, Request
from api.bdd.connexion import SessionLocal
from api.bdd.security import get_current_user
from api.schema.ProduitsSchema import ProduitsSchema
from api.controller import ProduitsController


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#--------------route Produits--------------------#

@router.get("/produits" , tags=["produits"], response_model=list[ProduitsSchema])
async def get_produits(db: Session = Depends(get_db)):
    return ProduitsController.get_all_produits(db=db)

@router.post("/produits/{id}", tags=["produits"])
async def get_one_produit(id: int, db: Session = Depends(get_db)):
    return ProduitsController.one_produit(db=db, produits_id=id)

@router.post("/produits", tags=["produits"])
async def create_produits(
        request: Request,
        nom: str = Form(...),
        prix: str = Form(...),
        categorie: str = Form(...),
        description: str = Form(...),
        statut: str = Form(...),
        quantite: int = Form(...),
        images: UploadFile = File(...),
        db: Session = Depends(get_db)
):

    return await ProduitsController.create_produits(
        db=db,
        nom=nom,
        prix=prix,
        categorie=categorie,
        description=description,
        statut=statut,
        quantite=quantite,
        images=images,
        request=request
    )

@router.put("/produits/{id}", tags=["produits"])
async def update_produits(id: int, produits: ProduitsSchema, db: Session = Depends(get_db)):
    return ProduitsController.update_produits(db=db, produits=produits, produits_id=id)

@router.delete("/produits/{id}", tags=["produits"])
async def delete_produits(id: int, db: Session = Depends(get_db)):
    return ProduitsController.delete_produits(db=db, id=id)


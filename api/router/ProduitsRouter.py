from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends,Form, UploadFile,File
from api.bdd.connexion import SessionLocal
from api.schema.ProduitsSchema import ProduitsSchema
from api.controller import ProduitsController


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#--------------route Produits--------------------#

@router.get("/produits" , tags=["produits"], response_model=list[ProduitsSchema])
async def get_produits():
    return ProduitsController.get_all_produits(db=SessionLocal())

@router.post("/produits/{id}", tags=["produits"])
async def get_one_produit(id: int):
    db=SessionLocal()
    return ProduitsController.one_produit(db=db, produits_id=id)

@router.post("/produits", tags=["produits"])
async def create_produits(
        nom: str = Form(...),
        prix: str = Form(...),
        categorie: str = Form(...),
        description: str = Form(...),
        statut: str = Form(...),
        quantite: str = Form(...),
        images: UploadFile = File(...)
):
    db=SessionLocal()
    return ProduitsController.create_produits(
        db=db,
        nom=nom,
        prix=prix,
        categorie=categorie,
        description=description,
        statut=statut,
        quantite=quantite,
        images=images,

    )

@router.put("/produits/{id}", tags=["produits"])
async def update_produits(id: int, produits: ProduitsSchema):
    db=SessionLocal()
    return ProduitsController.update_produits(db=db, produits=produits, produits_id=id)

@router.delete("/produits/{id}", tags=["produits"])
async def delete_produits(id: int):
    db=SessionLocal()
    return ProduitsController.delete_produits(db=db, id=id)


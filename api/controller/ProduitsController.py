import os

from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, Form, File
from ..model.ProduitsModel import Produits
from ..model import ProduitsModel
from ..schema import ProduitsSchema
from ..schema.ProduitsSchema import ProduitsSchema

UPLOAD_DIR = "uploads/produits"
os.makedirs(UPLOAD_DIR, exist_ok=True)

#------------------------------------requetes crud produits--------------------------------#

def get_all_produits(db: Session):
    return db.query(ProduitsModel.Produits).all()

def create_produits(
        db: Session,
        nom: str = Form(...),
        prix: str = Form(...),
        categorie: str = Form(...),
        description: str = Form(...),
        statut: str = Form(...),
        quantite: str = Form(...),
        images: UploadFile = File(...)
    ):
    if not images.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Format non supporté : image uniquement"
        )
    filename = f"produit_{nom}_{images.filename}"
    upload_dir = "uploads/produits"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(images.file.read())

        # Chemin relatif pour la DB
    relative_path = f"uploads/produits/{filename}"

    # URL publique accessible
    image_url = f"http://127.0.0.1:8000/{relative_path}"

    new_produits = Produits(
        nom=nom,
        prix = prix,
        categorie = categorie,
        description = description,
        statut = statut,
        quantite = quantite,
        images = relative_path,
    )

    db.add(new_produits)
    db.commit()
    db.refresh(new_produits)


    return {
        "message": "Produit créé",
        "produit": new_produits,
        "image_url": image_url
    }

def update_produits(db: Session, produits_id: int, produits: ProduitsSchema):

    db_produits = db.query(Produits).filter(Produits.id == produits_id).first()
    if not db_produits:
        raise HTTPException(status_code=404, detail="Produits non trouvé")

    for key, value in produits.dict().items():
        setattr(db_produits, key, value)

    db.commit()
    db.refresh(db_produits)

    return {
        "message": "produits mis à jour avec succès",
        "detail": "success",
        "produits": db_produits
    }

def one_produit(db: Session, produits_id: int):
    produit = db.query(Produits).filter(Produits.id == produits_id).first()
    if not produit:
        raise HTTPException(status_code=404, detail="Produits non trouv<UNK>")
    return produit

def delete_produits(db: Session, id: int):
    del_produits = db.query(Produits).filter(Produits.id == id).first()
    if not del_produits:
        raise HTTPException(status_code=404, detail="Produits non trouvé")
    db.delete(del_produits)
    db.commit()

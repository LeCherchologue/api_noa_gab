from sqlalchemy.sql.functions import current_user
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from ..model.CommandesModel import Commandes
from ..model import CommandesModel, ProduitsModel
from ..schema import CommandesSchema

#------------------------------------requetes crud commandes--------------------------------#

def get_all_commandes(db: Session):
    return db.query(CommandesModel.Commandes).all()

def create_commandes(db: Session, commandes: CommandesSchema):


    db_produit = db.query(ProduitsModel.Produits).filter(ProduitsModel.Produits.id == commandes.produit_id).first()

    if not db_produit:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    if int(db_produit.quantite) < commandes.quantite:
        raise HTTPException(
            status_code=400,
            detail=f"Stock insuffisant : disponible {db_produit.quantite}, demandé {commandes.quantite}"
        )


    new_commandes = Commandes(**commandes.dict())

    db.add(new_commandes)
    qte = int(db_produit.quantite)
    qte -= commandes.quantite

    db.commit()
    db.refresh(new_commandes)

    return {
        "message": "commandes cree",
        "detail": "success",
        "commandes": new_commandes
    }

def update_commandes(db: Session, commandes_id: int, commandes: CommandesSchema):

    db_commandes = db.query(Commandes).filter(Commandes.id == commandes_id).first()
    if not db_commandes:
        raise HTTPException(status_code=404, detail="Commandes non trouvé")

    for key, value in commandes.dict().items():
        setattr(db_commandes, key, value)

    db.commit()
    db.refresh(db_commandes)

    return {
        "message": "commandes mis à jour avec succès",
        "detail": "success",
        "commandes": db_commandes
    }

def delete_commandes(db: Session, id: int):
    del_commandes = db.query(Commandes).filter(Commandes.id == id).first()
    if not del_commandes:
        raise HTTPException(status_code=404, detail="Commandes non trouvé")
    db.delete(del_commandes)
    db.commit()

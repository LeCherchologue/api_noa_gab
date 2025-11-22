
from sqlalchemy import Column, Integer, String, func, DateTime, Boolean, ForeignKey,Date
from sqlalchemy.orm import relationship
from ..bdd.connexion import Base

class Produits(Base):
    __tablename__ = "produits"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String(255))
    prix = Column(String(255))
    categorie = Column(String(255))
    description = Column(String(255))
    statut = Column(String(255))
    quantite = Column(String(255))
    images = Column(String(255))
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), nullable=False)

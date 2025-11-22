
from sqlalchemy import Column, Integer, String, func, DateTime, Boolean, ForeignKey,Date
from sqlalchemy.orm import relationship
from ..bdd.connexion import Base

class Commandes(Base):
    __tablename__ = "commandes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quantite = Column(Integer)
    total = Column(Integer)
    produit_id = Column(Integer, ForeignKey("produits.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), nullable=False)

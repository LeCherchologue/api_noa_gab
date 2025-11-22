
from sqlalchemy import Column, Integer, String, func, DateTime, Boolean, ForeignKey,Date
from sqlalchemy.orm import relationship
from ..bdd.connexion import Base

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String(255))
    prenom = Column(String(255))
    email = Column(String(255))
    tel = Column(String(255))
    adresse = Column(String(255))
    profil = Column(String(255))
    password = Column(String(100))
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), nullable=False)

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status

from ..bdd.security import create_access_token
from ..model.UsersModel import Users
from ..model import UsersModel
from ..schema import UsersSchema

from passlib.context import CryptContext

pwd_crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


#------------------------------------requetes authentification--------------------------------#

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, form_data: OAuth2PasswordRequestForm):
    db_user = db.query(Users).filter(
        Users.email == form_data.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )

    token = create_access_token({
        "user_id": db_user.id,
        "email": db_user.email,
        "profil": db_user.profil
    })

    return {
        "success": True,
        "message": "Connexion réussie",
        "access_token": token,
        "token_type": "bearer",
        "data": {
            "id": db_user.id,
            "nom": db_user.nom,
            "prenom": db_user.prenom,
            "tel": db_user.tel,
            "adresse": db_user.adresse,
            "email": db_user.email,
            "profil": db_user.profil,
        }
    }

#------------------------------------requetes crud users--------------------------------#

def get_all_users(db: Session):
    return db.query(UsersModel.Users).all()

def create_users(db: Session, users: UsersSchema.UsersSchema):
    print("PASSWORD =", users.password, "LEN =", len(users.password))

    new_users = Users(
        nom=users.nom,
        prenom = users.prenom,
        email = users.email,
        tel = users.tel,
        adresse = users.adresse,
        profil = users.profil,
        password = hash_password(users.password),
    )
    print(new_users)
    db.add(new_users)
    db.commit()
    db.refresh(new_users)

    return {
        "message": "users cree",
        "detail": "success",
        "users": new_users
    }


def update_users(db: Session, users_id: int, users: UsersSchema):

    db_users = db.query(Users).filter(Users.id == users_id).first()
    if not db_users:
        raise HTTPException(status_code=404, detail="Users non trouvé")

    for key, value in users.dict().items():
        setattr(db_users, key, value)

    db.commit()
    db.refresh(db_users)

    return {
        "message": "users mis à jour avec succès",
        "detail": "success",
        "users": db_users
    }

def delete_users(db: Session, id: int):
    del_users = db.query(Users).filter(Users.id == id).first()
    if not del_users:
        raise HTTPException(status_code=404, detail="Users non trouvé")
    db.delete(del_users)
    db.commit()

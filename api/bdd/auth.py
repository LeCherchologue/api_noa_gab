from fastapi import HTTPException, Request, status
from jose import jwt, JWTError

SECRET_KEY = "MON_SUPER_SECRET"
ALGORITHM = "HS256"


def get_token_from_header(request: Request):
    """
    Extrait le token du header Authorization: Bearer <token>
    """
    header = request.headers.get("Authorization")

    if not header or not header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="non authorized",
        )

    return header.split(" ")[1]


def verify_token(token: str):
    """
    Vérifie le token JWT
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide"
        )

# app/routers/app.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas import Usuario, Credenciais
from app import models
from app.core.security import create_access_token, decode_access_token
from app.core.database import get_db


router = APIRouter()
bearer_scheme = HTTPBearer()

@router.post("/registrar")
def registrar(usuario: Usuario, db: Session = Depends(get_db)):
    if models.get_user_by_email(db, usuario.email):
        raise HTTPException(status_code=409, detail="Email já cadastrado")
    user = models.create_user(db, usuario)
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
def login(cred: Credenciais, db: Session = Depends(get_db)):
    if not models.authenticate_user(db, cred.email, cred.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(data={"sub": cred.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/consultar")
def consultar(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    email = decode_access_token(token)
    # você pode buscar dados do usuário ou usar db em outras queries
    dados_externos = [ ... ]
    return {"usuario": email, "dados": dados_externos}

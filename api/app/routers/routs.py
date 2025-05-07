# app/routers/app.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas import Usuario, Credenciais
from app import models
from app.core.security import create_access_token, decode_access_token

router = APIRouter()
bearer_scheme = HTTPBearer()   # novo: HTTPBearer em vez de OAuth2PasswordBearer

@router.post("/registrar")
def registrar(usuario: Usuario):
    if usuario.email in models.usuarios_db:
        raise HTTPException(status_code=409, detail="Email já cadastrado")
    models.create_user(usuario.nome, usuario.email, usuario.senha)
    token = create_access_token(data={"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
def login(cred: Credenciais):
    if not models.authenticate_user(cred.email, cred.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(data={"sub": cred.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/consultar")
def consultar(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    # extrai o token puro do header "Authorization: Bearer <token>"
    token = credentials.credentials
    # decodifica e valida
    email = decode_access_token(token)
    dados_externos = [
        {"data": "2025-05-01", "valor": 123},
        {"data": "2025-05-02", "valor": 456},
        {"data": "2025-05-03", "valor": 789},
    ]
    return {"usuario": email, "dados": dados_externos}

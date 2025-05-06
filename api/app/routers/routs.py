# app/routers/app.py
from fastapi import APIRouter, HTTPException, Header
from app.schemas import Usuario, Credenciais
from app import models

router = APIRouter()

@router.post("/registrar")
def registrar(usuario: Usuario):
    if usuario.email in models.usuarios_db:
        raise HTTPException(status_code=409, detail="Email já cadastrado")
    models.usuarios_db[usuario.email] = {
        "nome": usuario.nome,
        "senha": usuario.senha
    }
    return {"jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.exemplo.de.token.jwt"}

@router.post("/login")
def login(cred: Credenciais):
    user = models.usuarios_db.get(cred.email)
    if not user or user["senha"] != cred.senha:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    return {"jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.exemplo.de.token.jwt"}

@router.get("/consultar")
def consultar(Authorization: str = Header(None)):
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Token JWT ausente ou inválido")
    return {
        "dados": [
            {"data": "2025-05-01", "valor": 123},
            {"data": "2025-05-02", "valor": 456},
            {"data": "2025-05-03", "valor": 789}
        ]
    }

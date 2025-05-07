# api/app/models.py
from typing import Dict
from app.core.security import get_password_hash, verify_password

# “banco” em memória: email → { nome, senha_hash }
usuarios_db: Dict[str, Dict[str, str]] = {}

def create_user(nome: str, email: str, senha: str) -> None:
    hashed = get_password_hash(senha)
    usuarios_db[email] = { "nome": nome, "senha": hashed }

def authenticate_user(email: str, senha: str) -> bool:
    user = usuarios_db.get(email)
    if not user:
        return False
    return verify_password(senha, user["senha"])

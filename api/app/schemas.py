# app/schemas.py
from pydantic import BaseModel

class Usuario(BaseModel):
    nome: str
    email: str
    senha: str

class Credenciais(BaseModel):
    email: str
    senha: str

# app/models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from app.core.database import Base
from app.core.security import get_password_hash, verify_password
from app.schemas import Usuario

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    senha = Column(String(255), nullable=False)  # já será o hash

# funções de CRUD:

def create_user(db: Session, user: Usuario):
    hashed = get_password_hash(user.senha)
    db_user = User(nome=user.nome, email=user.email, senha=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, senha: str) -> bool:
    user = get_user_by_email(db, email)
    if not user:
        return False
    return verify_password(senha, user.senha)

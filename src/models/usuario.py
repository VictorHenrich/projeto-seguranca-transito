from sqlalchemy import Column, String, Boolean, Date, DateTime, Integer
from datetime import date, datetime

from .base_model import BaseModel


class Usuario(BaseModel):
    __tablename__: str = "usuarios"

    nome: str = Column(String(150), nullable=False)
    email: str = Column(String(250), nullable=False, unique=True)
    senha: str = Column(String(50), nullable=False)
    cpf: str = Column(String(20), nullable=False, unique=True)
    data_nascimento: date = Column(Date)
    data_cadastro: datetime = Column(DateTime, default=datetime.now)
    ativo: bool = Column(Boolean, default=True)

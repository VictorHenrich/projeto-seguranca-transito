from sqlalchemy import String, Boolean, Date, DateTime, Integer
from sqlalchemy.orm import mapped_column, Mapped
from datetime import date, datetime

from .base_model import BaseModel


class User(BaseModel):
    __tablename__: str = "usuarios"

    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    senha: Mapped[str] = mapped_column(String(50), nullable=False)
    cpf: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    data_nascimento: Mapped[date] = mapped_column(Date)
    data_cadastro: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)

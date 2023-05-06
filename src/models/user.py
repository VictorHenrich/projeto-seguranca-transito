from sqlalchemy import String, Boolean, Date, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from datetime import date, datetime

from .base_model import BaseModel


class User(BaseModel):
    __tablename__: str = "usuarios"

    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    senha: Mapped[str] = mapped_column(String(50), nullable=False)
    cpf: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    rg: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    estado_emissor: Mapped[str] = mapped_column(String(50), nullable=False)
    data_nascimento: Mapped[date] = mapped_column(Date)
    data_cadastro: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    uf: Mapped[str] = mapped_column(String(2), nullable=False)
    cidade: Mapped[str] = mapped_column(String(200), nullable=False)
    bairro: Mapped[str] = mapped_column(String(200), nullable=False)
    logradouro: Mapped[str] = mapped_column(String(200), nullable=False)
    numero: Mapped[str] = mapped_column(String(30), nullable=False, defauilt="0")

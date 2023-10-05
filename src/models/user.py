from sqlalchemy import String, Date, DateTime
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
    telefone: Mapped[str] = mapped_column(String(20), nullable=False)
    estado_emissor: Mapped[str] = mapped_column(String(50), nullable=False)
    data_nascimento: Mapped[date] = mapped_column(Date, nullable=False)
    data_cadastro: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    endereco_uf: Mapped[str] = mapped_column(String(2), nullable=False)
    endereco_cidade: Mapped[str] = mapped_column(String(200), nullable=False)
    endereco_bairro: Mapped[str] = mapped_column(String(200), nullable=False)
    endereco_logradouro: Mapped[str] = mapped_column(String(200), nullable=False)
    endereco_numero: Mapped[str] = mapped_column(
        String(30), nullable=False, default="0"
    )
    endereco_cep: Mapped[str] = mapped_column(String(30), nullable=False)

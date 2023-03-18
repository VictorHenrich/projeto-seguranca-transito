from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from .base_model import BaseModel


class Departament(BaseModel):
    __tablename__: str = "departamentos"

    nome: Mapped[str] = mapped_column(String(250), nullable=False)
    unidade: Mapped[str] = mapped_column(String(200))
    acesso: Mapped[str] = mapped_column(String(200))
    cep: Mapped[str] = mapped_column(String(20), nullable=False)
    uf: Mapped[str] = mapped_column(String(250), nullable=False)
    cidade: Mapped[str] = mapped_column(String(250), nullable=False)
    bairro: Mapped[str] = mapped_column(String(250), nullable=False)
    logradouro: Mapped[str] = mapped_column(String(250), nullable=False)
    complemento: Mapped[str] = mapped_column(String(250))

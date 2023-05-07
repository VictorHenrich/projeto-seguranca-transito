from typing import Optional
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import mapped_column, Mapped

from .base_model import BaseModel


class Vehicle(BaseModel):
    __tablename__: str = "veiculos_usuario"

    placa: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    renavam: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    tipo_veiculo: Mapped[str] = mapped_column(String(50), nullable=False)
    marca: Mapped[Optional[str]] = mapped_column(String(50))
    modelo: Mapped[Optional[str]] = mapped_column(String(50))
    cor: Mapped[Optional[str]] = mapped_column(String(50))
    ano: Mapped[Optional[int]] = mapped_column(Integer)
    chassi: Mapped[Optional[str]] = mapped_column(String(50))
    possui_seguro: Mapped[Boolean] = mapped_column(Boolean, default=False)

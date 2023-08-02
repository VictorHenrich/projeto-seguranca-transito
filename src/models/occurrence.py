from typing import Optional
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from .base_model import BaseModel
from .user import User
from .vehicle import Vehicle


class Occurrence(BaseModel):
    __tablename__: str = "ocorrencias"

    id_usuario: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{User.__tablename__}.id"), nullable=False
    )
    id_veiculo: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{Vehicle.__tablename__}.id"), nullable=False
    )
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    codigo_externo: Mapped[Optional[str]] = mapped_column(String(100))
    data_cadastro: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pendente")
    endereco_uf: Mapped[str] = mapped_column(String(2), nullable=False, default="SC")
    endereco_cidade: Mapped[str] = mapped_column(String(200), nullable=False)
    endereco_bairro: Mapped[str] = mapped_column(String(200), nullable=False)
    endereco_logragouro: Mapped[str] = mapped_column(String(300), nullable=False)
    endereco_numero: Mapped[str] = mapped_column(String(10), nullable=False)
    latitude: Mapped[str] = mapped_column(String(300), nullable=False)
    longitude: Mapped[str] = mapped_column(String(300), nullable=False)
    obs: Mapped[str] = mapped_column(Text, nullable=False)

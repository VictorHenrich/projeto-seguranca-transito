from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from .base_model import BaseModel
from .departament import Departament


class Agent(BaseModel):
    __tablename__: str = "usuarios_departamentos"

    id_departamento: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{Departament.__tablename__}.id"), nullable=False
    )
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    acesso: Mapped[str] = mapped_column(String(150), nullable=False)
    senha: Mapped[str] = mapped_column(String(100), nullable=False)
    cargo: Mapped[str] = mapped_column(String(200), nullable=False)
    data_cadastro: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )

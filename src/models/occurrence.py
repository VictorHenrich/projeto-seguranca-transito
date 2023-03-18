from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from .base_model import BaseModel
from .user import User
from .departament import Departament


class Occurrence(BaseModel):
    __tablename__: str = "ocorrencias"

    id_usuario: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{User.__tablename__}.id"), nullable=False
    )
    id_departamento: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{Departament.__tablename__}.id"), nullable=False
    )
    descricao: Mapped[str] = mapped_column(String(200), nullable=False)
    obs: Mapped[str] = mapped_column(String(5000))
    data_cadastro: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pendente")

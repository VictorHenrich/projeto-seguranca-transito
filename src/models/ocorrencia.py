from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime

from .base_model import BaseModel
from .usuario import Usuario
from .departamento import Departamento


class Ocorrencia(BaseModel):
    __tablename__: str = "ocorrencias"

    id_usuario: int = Column(
        Integer, ForeignKey(f"{Usuario.__tablename__}.id"), nullable=False
    )
    id_departamento: int = Column(
        Integer, ForeignKey(f"{Departamento.__tablename__}.id"), nullable=False
    )
    descricao: str = Column(String(200), nullable=False)
    obs: str = Column(String(5000))
    data_cadastro: datetime = Column(DateTime, nullable=False, default=datetime.now)
    status: str = Column(String(20), nullable=False, default="pendente")

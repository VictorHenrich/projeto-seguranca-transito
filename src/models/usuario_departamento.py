from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

from .base_model import BaseModel
from .departamento import Departamento



class UsuarioDepartamento(BaseModel):
    __tablename__: str = "usuarios_departamentos"

    id_departamento: int = Column(
        Integer, ForeignKey(f"{Departamento.__tablename__}.id"), nullable=False
    )
    nome: str = Column(String(200), nullable=False)
    acesso: str = Column(String(150), nullable=False)
    senha: str = Column(String(100), nullable=False)
    cargo: str = Column(String(200), nullable=False)
    data_cadastro: datetime = Column(DateTime, default=datetime.now, nullable=False)

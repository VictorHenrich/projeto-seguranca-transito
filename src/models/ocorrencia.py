from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey
)
from datetime import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from start import server
from services.database import Database
from .usuario import Usuario
from .departamento import Departamento
from .tipo_ocorrencia import TipoOcorrencia



db: Database = server.databases.get_database()


class Ocorrencia(db.Model):
    __tablename__:str = "ocorrencias"

    id: int = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    id_usuario: int = Column(Integer, ForeignKey(f"{Usuario.__tablename__}.id"), nullable=False)
    id_departamento: int = Column(Integer, ForeignKey(f"{Departamento.__tablename__}.id"), nullable=False)
    id_tipo: int = Column(Integer, ForeignKey(f"{TipoOcorrencia.__tablename__}.id"))
    id_uuid: str = Column(UUID(False), unique=True, nullable=False, default=lambda _: str(uuid4()))
    descricao: str = Column(String(200), nullable=False)
    obs: str = Column(String(5000))
    data_cadastro: datetime = Column(DateTime, nullable=False, default=datetime.now)
    status: str = Column(String(20), nullable=False, default="pendente")
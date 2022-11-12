from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey
)
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from start import server
from services.database import Database
from .nivel import Nivel


db: Database = server.databases.get_database()


class TipoOcorrencia(db.Model):
    __tablename__: str = "tipos_ocorrencias"

    id: int = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    id_uuid: str = Column(UUID(False), unique=True, nullable=False, default=lambda _: str(uuid4()))
    id_nivel: int = Column(Integer, ForeignKey(f"{Nivel.__tablename__}.id"), nullable=False)
    descricao: str = Column(String(200), nullable=False)
    instrucao: str = Column(String(20000))

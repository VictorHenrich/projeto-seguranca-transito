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
from .departamento import Departamento


db: Database = server.databases.get_database()


class Nivel(db.Model):
    __tablename__: str = "niveis"

    id: int = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    id_uuid: str = Column(UUID(False), unique=True, nullable=False, default=lambda _: str(uuid4()))
    id_departamento: int = Column(Integer, ForeignKey(f"{Departamento.__tablename__}.id"))
    descricao: str = Column(String(20), nullable=False)
    obs: str = Column(String(5000))
    nivel: int = Column(Integer, default=0, nullable=False)
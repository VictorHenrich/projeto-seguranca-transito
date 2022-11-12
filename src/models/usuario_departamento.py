from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)
from datetime import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from start import server
from services.database import Database
from models import Departamento


db: Database = server.databases.get_database()


class UsuarioDepartamento(db.Model):
    __tablename__: str = "usuarios_departamentos"

    id: int = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    id_uuid: str = Column(UUID(False), unique=True, nullable=False, default=uuid4)
    id_departamento: int = Column(Integer, ForeignKey(f"{Departamento.__tablename__}.id"), nullable=False)
    nome: str = Column(String(200), nullable=False)
    acesso: str = Column(String(150), nullable=False)
    senha: str = Column(String(100), nullable=False)
    cargo: str = Column(String(200), nullable=False)
    data_cadastro: datetime = Column(DateTime, default=datetime.now, nullable=False)
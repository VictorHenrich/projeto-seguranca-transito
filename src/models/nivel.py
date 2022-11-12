from sqlalchemy import (
    Column,
    String,
    Integer
)
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from start import server
from services.database import Database


db: Database = server.databases.get_database()


class Nivel(db.Model):
    __tablename__: str = "niveis"

    id: int = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    id_uuid: str = Column(UUID(False), unique=True, nullable=False, default=uuid4)
    descricao: str = Column(String(20), nullable=False)
    obs: str = Column(String(5000))
    nivel: int = Column(Integer, default=0, nullable=False)
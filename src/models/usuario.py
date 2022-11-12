from sqlalchemy import (
    Column,
    String,
    Boolean,
    Date,
    DateTime,
    Integer
)

from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import date, datetime
from services.database import Database
from start import server



db: Database = server.databases.get_database()



class Usuario(db.Model):
    __tablename__: str = "usuarios"

    id: int = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    id_uuid: str = Column(UUID(False), unique=True, nullable=False, default=lambda _: str(uuid4()))
    nome: str = Column(String(150), nullable=False)
    email: str = Column(String(250), nullable=False, unique=True)
    senha: str = Column(String(50), nullable=False)
    cpf: str = Column(String(20), nullable=False, unique=True)
    data_nascimento: date = Column(Date)
    data_cadastro: datetime = Column(DateTime, default=datetime.now)
    ativo: bool = Column(Boolean, default=True)

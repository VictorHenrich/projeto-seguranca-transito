from sqlalchemy import (
    Column,
    Integer,
    String
)
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from start import server
from services.database import Database



db: Database = server.databases.get_database()



class Departamento(db.Model):
    __tablename__: str = "departamentos"

    id: int = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    id_uuid: str = Column(UUID(False), unique=True, nullable=False, default=lambda _: str(uuid4()))
    codigo: int = Column(Integer, nullable=False, autoincrement=True, unique=True)
    nome: str = Column(String(250), nullable=False)
    unidade: str = Column(String(200))
    acesso: str = Column(String(200))
    cep: str = Column(String(20), nullable=False)
    uf: str = Column(String(250), nullable=False)
    cidade: str = Column(String(250), nullable=False)
    bairro: str = Column(String(250), nullable=False)
    logradouro: str = Column(String(250), nullable=False)
    complemento: str = Column(String(250))
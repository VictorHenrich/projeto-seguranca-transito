from sqlalchemy import Column, Integer, String

from .base_model import BaseModel


class Departamento(BaseModel):
    __tablename__: str = "departamentos"

    nome: str = Column(String(250), nullable=False)
    unidade: str = Column(String(200))
    acesso: str = Column(String(200))
    cep: str = Column(String(20), nullable=False)
    uf: str = Column(String(250), nullable=False)
    cidade: str = Column(String(250), nullable=False)
    bairro: str = Column(String(250), nullable=False)
    logradouro: str = Column(String(250), nullable=False)
    complemento: str = Column(String(250))

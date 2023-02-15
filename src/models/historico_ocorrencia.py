from sqlalchemy import Column, Float, Integer, ForeignKey
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from start import app
from server.database import Database
from .ocorrencia import Ocorrencia


db: Database = app.databases.get_database()


class HistoricoOcorrencia(db.Model):
    __tablename__: str = "historicos_localizacao"

    id: int = Column(
        Integer, primary_key=True, nullable=False, autoincrement=True, unique=True
    )
    id_uuid: str = Column(
        UUID(False), unique=True, nullable=False, default=lambda _: str(uuid4())
    )
    id_ocorrencia: int = Column(
        Integer, ForeignKey(f"{Ocorrencia.__tablename__}.id"), nullable=False
    )
    latitude: float = Column(Float, nullable=False)
    longitude: float = Column(Float, nullable=False)

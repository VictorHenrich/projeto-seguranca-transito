from sqlalchemy import Column, Float, Integer, ForeignKey

from .base_model import BaseModel
from .ocorrencia import Ocorrencia


class HistoricoOcorrencia(BaseModel):
    __tablename__: str = "historicos_localizacao"

    id_ocorrencia: int = Column(
        Integer, ForeignKey(f"{Ocorrencia.__tablename__}.id"), nullable=False
    )
    latitude: float = Column(Float, nullable=False)
    longitude: float = Column(Float, nullable=False)

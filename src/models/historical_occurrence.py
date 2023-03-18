from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base_model import BaseModel
from .occurrence import Occurrence


class HistoricalOccurrence(BaseModel):
    __tablename__: str = "historicos_localizacao"

    id_ocorrencia: Mapped[int] = mapped_column(
        ForeignKey(f"{Occurrence.__tablename__}.id"), nullable=False
    )
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

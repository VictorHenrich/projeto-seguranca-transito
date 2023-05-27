from typing import Optional
from sqlalchemy import Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base_model import BaseModel
from .occurrence import Occurrence


class Attachment(BaseModel):
    __tablename__: str = "anexos_ocorrencia"

    id_ocorrencia: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{Occurrence.__tablename__}.id"), nullable=False
    )
    caminho_interno: Mapped[Optional[str]] = mapped_column(Text)
    url: Mapped[Optional[str]] = mapped_column(Text)

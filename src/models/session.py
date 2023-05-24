from typing import Optional
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from .base_model import BaseModel
from .user import User


class Session(BaseModel):
    __tablename__: str = "sessoes"

    id_usuario: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(f"{User.__tablename__}.id"),
        nullable=False,
        primary_key=True,
    )
    id_socket: Mapped[Optional[str]] = mapped_column(String(300))
    data_login: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    data_logout: Mapped[Optional[datetime]] = mapped_column(DateTime)

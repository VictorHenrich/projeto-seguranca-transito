from typing import Mapping, Any
from uuid import uuid4
from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from server.database import Database, Databases

database: Database = Databases.get_database()


class BaseModel(database.Base):
    __abstract__: bool = True

    __table_args__: Mapping[str, Any] = {"extend_existing": True}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, unique=True, nullable=False
    )
    id_uuid: Mapped[str] = mapped_column(
        UUID(False), unique=True, nullable=False, default=lambda _: str(uuid4())
    )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id} uuid='{self.id_uuid}'"

from uuid import uuid4
from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from server import App
from server.database import Database


database: Database = App.databases().get_database()


class BaseModel(database.Base):
    __abstract__: bool = True

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, unique=True, nullable=False
    )
    id_uuid: Mapped[str] = mapped_column(
        UUID(False), unique=True, nullable=False, default=lambda _: str(uuid4())
    )

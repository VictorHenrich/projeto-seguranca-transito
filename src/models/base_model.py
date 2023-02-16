from uuid import uuid4
from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import UUID

from start import app
from server.database import Database


database: Database = app.databases.get_database()


class BaseModel(database.Model):
    __abstract__: bool = True

    id: int = Column(Integer, primary_key=True, nullable=False, unique=True)
    id_uuid: str = Column(
        UUID(False), unique=True, nullable=False, default=lambda _: str(uuid4())
    )

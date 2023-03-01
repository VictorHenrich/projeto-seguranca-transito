from typing import Protocol, Dict, Any, Union, Sequence

from sqlalchemy.orm.session import Session
from sqlalchemy.ext.asyncio import AsyncSession


class IDatabase(Protocol):
    def create_session(
        self, *args: Sequence[Any], **options: Dict[str, Any]
    ) -> Union[Session, AsyncSession]:
        ...

    def migrate(self, drop_tables: bool, *args: Sequence[Any]) -> None:
        ...

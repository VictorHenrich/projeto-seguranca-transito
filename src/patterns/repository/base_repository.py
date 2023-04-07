from abc import ABC
from sqlalchemy.orm import Session


class BaseRepository(ABC):
    def __init__(self, session: Session) -> None:
        self.__session: Session = session

    @property
    def session(self) -> Session:
        return self.__session

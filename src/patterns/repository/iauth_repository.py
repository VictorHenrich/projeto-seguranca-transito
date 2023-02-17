from typing import Protocol, Generic, TypeVar

from models import BaseModel


T = TypeVar("T")

M = TypeVar("M", bound=BaseModel)


class IAuthRepository(Protocol, Generic[T, M]):
    def auth(self, params: T) -> M:
        pass

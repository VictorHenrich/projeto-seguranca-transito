from typing import Protocol, Generic, TypeVar

from models import BaseModel


T = TypeVar("T", contravariant=True)
M = TypeVar("M", bound=BaseModel, covariant=True)


class IAuthRepository(Protocol, Generic[T, M]):
    def auth(self, params: T) -> M:
        ...

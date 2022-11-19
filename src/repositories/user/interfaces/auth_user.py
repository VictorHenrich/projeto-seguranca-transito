from typing import Protocol



class IUserAuthorization(Protocol):
    email: str
    password: str
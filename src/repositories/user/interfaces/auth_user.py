from typing import Protocol



class UserAuth(Protocol):
    email: str
    password: str
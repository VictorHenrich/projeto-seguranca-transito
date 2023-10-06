from dataclasses import dataclass


@dataclass
class UserAuthPayload:
    email: str
    password: str

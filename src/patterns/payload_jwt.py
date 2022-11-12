from dataclasses import dataclass


@dataclass
class PayloadJWT:
    uuid_user: str
    expired: float



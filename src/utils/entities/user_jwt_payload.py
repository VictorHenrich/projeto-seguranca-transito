from dataclasses import dataclass


@dataclass
class PayloadUserJWT:
    user_uuid: str
    expired: float

from dataclasses import dataclass



@dataclass
class PayloadUserJWT:
    uuid_user: str
    expired: float
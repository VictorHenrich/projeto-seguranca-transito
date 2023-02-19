from dataclasses import dataclass


@dataclass
class PayloadDepartamentUserJWT:
    uuid_user: str
    uuid_departament: str
    expired: float

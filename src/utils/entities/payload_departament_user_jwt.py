from dataclasses import dataclass


@dataclass
class PayloadDepartamentUserJWT:
    user_uuid: str
    uuid_departament: str
    expired: float

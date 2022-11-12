from dataclasses import dataclass



@dataclass
class UserAuthentication:
    email: str
    senha: str
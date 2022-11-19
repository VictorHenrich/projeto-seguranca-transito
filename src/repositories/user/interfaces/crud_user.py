from typing import Protocol, Union
from datetime import date



class IUserRegistration(Protocol):
    name: str
    email: str
    document: str
    password: str
    date_birth: Union[date, str]


class IUserLocation(Protocol):
    uuid: str
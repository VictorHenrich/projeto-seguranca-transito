from typing import Protocol, Union
from datetime import date



class UserWriteData(Protocol):
    name: str
    email: str
    document: str
    password: str
    date_birth: Union[date, str]


class UserLocationData(Protocol):
    uuid: str
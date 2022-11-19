from dataclasses import dataclass
from typing import Union
from datetime import date


@dataclass
class UserRegistration:
    name: str
    email: str
    document: str
    password: str
    date_birth: Union[date, str]


@dataclass
class UserLocation:
    uuid: str


@dataclass
class UserUpgrade:
    data: UserRegistration
    location_data: UserLocation
from typing import Union
from decimal import Decimal
from dataclasses import dataclass


@dataclass
class LocationPayload:
    lat: Union[str, float, Decimal]
    lon: Union[str, float, Decimal]

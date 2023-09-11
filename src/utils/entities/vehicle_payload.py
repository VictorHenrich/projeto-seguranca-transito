from typing import Optional
from dataclasses import dataclass
from ..types import VehicleTypes


@dataclass
class VehiclePayload:
    plate: str
    renavam: str
    vehicle_type: VehicleTypes
    brand: Optional[str] = None
    model: Optional[str] = None
    color: Optional[str] = None
    year: Optional[int] = None
    chassi: Optional[str] = None
    have_safe: bool = False

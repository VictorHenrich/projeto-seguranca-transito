from dataclasses import dataclass


@dataclass
class AddressPayload:
    zipcode: str
    state: str
    city: str
    district: str
    street: str
    number: str = ""

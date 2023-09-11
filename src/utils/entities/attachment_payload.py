from typing import Union
from dataclasses import dataclass


@dataclass
class AttachmentPayload:
    content: Union[str, bytes]
    type: str

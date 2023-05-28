from typing import Protocol, Optional

from patterns.repository import BaseRepository
from models import Attachment
from exceptions import AttachmentNotFoundError


class AttachmentFindRepositoryParams(Protocol):
    attachment_uuid: str


class AttachmentFindRepository(BaseRepository):
    def find_one(self, params: AttachmentFindRepositoryParams) -> Attachment:
        attachment: Optional[Attachment] = (
            self.session.query(Attachment)
            .filter(Attachment.id_uuid == params.attachment_uuid)
            .first()
        )

        if not attachment:
            raise AttachmentNotFoundError()

        return attachment

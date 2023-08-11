from typing import Protocol, Collection

from patterns.repository import BaseRepository
from models import Attachment, Occurrence


class AttachmentFindManyRepositoryParams(Protocol):
    occurrence: Occurrence


class AttachmentFindManyRepository(BaseRepository):
    def find_many(
        self, params: AttachmentFindManyRepositoryParams
    ) -> Collection[Attachment]:
        return (
            self.session.query(Attachment)
            .join(Occurrence, Occurrence.id == Attachment.id_ocorrencia)
            .filter(Occurrence.id == params.occurrence.id)
            .all()
        )

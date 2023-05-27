from typing import Protocol, Optional
from patterns.repository import BaseRepository
from models import Occurrence, Attachment


class AttachmentCreateRepositoryParams(Protocol):
    occurrence: Occurrence
    internal_path: Optional[str]
    url: Optional[str]


class AttachmentCreateRepository(BaseRepository):
    def create(self, params: AttachmentCreateRepositoryParams) -> None:
        attachment: Attachment = Attachment()

        attachment.id_ocorrencia = params.occurrence.id
        attachment.caminho_interno = params.internal_path
        attachment.url = params.url

        self.session.add(attachment)

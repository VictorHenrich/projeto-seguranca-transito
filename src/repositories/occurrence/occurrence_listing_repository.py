from typing import List
from dataclasses import dataclass

from patterns.repository import BaseRepository
from models import Usuario, Ocorrencia


@dataclass
class OccurrenceListingRepositoryParam:
    user: Usuario


class OccurrenceListingRepository(BaseRepository):
    def list(self, param: OccurrenceListingRepositoryParam) -> List[Ocorrencia]:
        occurrences: List[Ocorrencia] = (
            self.session.query(Ocorrencia)
            .join(Usuario, Ocorrencia.id_usuario == Usuario.id)
            .filter(Ocorrencia.id_usuario == param.user.id)
            .all()
        )

        return occurrences

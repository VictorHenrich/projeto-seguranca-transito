from typing import List, Protocol

from patterns.repository import BaseRepository
from models import Usuario, Ocorrencia


class OccurrenceFindManyRepositoryParams(Protocol):
    user: Usuario


class OccurrenceFindManyRepository(BaseRepository):
    def list(self, params: OccurrenceFindManyRepositoryParams) -> List[Ocorrencia]:
        occurrences: List[Ocorrencia] = (
            self.session.query(Ocorrencia)
            .join(Usuario, Ocorrencia.id_usuario == Usuario.id)
            .filter(Ocorrencia.id_usuario == params.user.id)
            .all()
        )

        return occurrences

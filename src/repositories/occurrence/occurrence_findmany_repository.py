from typing import List, Protocol

from patterns.repository import BaseRepository
from models import User, Occurrence


class OccurrenceFindManyRepositoryParams(Protocol):
    user: User


class OccurrenceFindManyRepository(BaseRepository):
    def list(self, params: OccurrenceFindManyRepositoryParams) -> List[Occurrence]:
        occurrences: List[Occurrence] = (
            self.session.query(Occurrence)
            .join(User, Occurrence.id_usuario == User.id)
            .filter(Occurrence.id_usuario == params.user.id)
            .all()
        )

        return occurrences

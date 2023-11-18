from typing import Protocol, Tuple, TypeAlias, Collection, Sequence

from patterns.repository import BaseRepository
from models import Occurrence, User, Vehicle


OccurrenceLoad: TypeAlias = Sequence[Tuple[Occurrence, Vehicle]]


class OccurrenceAggregateRepositoryParams(Protocol):
    user: User


class OccurrenceAggregateRepository(BaseRepository):
    def find_many(
        self, params: OccurrenceAggregateRepositoryParams
    ) -> Collection[OccurrenceLoad]:
        return (
            self.session.query(Occurrence, Vehicle)
            .join(User, Occurrence.id_usuario == User.id)
            .join(Vehicle, Occurrence.id_veiculo == Vehicle.id)
            .filter(Occurrence.id_usuario == params.user.id)
            .all()
        )

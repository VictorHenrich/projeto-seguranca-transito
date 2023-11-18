from typing import Protocol, Tuple, TypeAlias, Collection

from patterns.repository import BaseRepository
from models import Occurrence, User, Vehicle


OccurrenceLoad: TypeAlias = Tuple[Occurrence, User, Vehicle]


class OccurrenceAggregateRepositoryParams(Protocol):
    occurrence_uuid: str


class OccurrenceAggregateRepository(BaseRepository):
    def find_one(
        self, params: OccurrenceAggregateRepositoryParams
    ) -> Collection[OccurrenceLoad]:
        return (
            self.session.query(Occurrence, User, Vehicle)
            .join(User, Occurrence.id_usuario == User.id)
            .join(Vehicle, Occurrence.id_veiculo == Vehicle.id)
            .filter(Occurrence.id_uuid == params.occurrence_uuid)
            .first()
        )

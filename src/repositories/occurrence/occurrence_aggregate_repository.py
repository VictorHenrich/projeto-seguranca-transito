from typing import Protocol, Optional, Tuple, TypeAlias
from sqlalchemy import Row

from patterns.repository import BaseRepository
from models import Occurrence, User, Vehicle
from exceptions import OccurrenceNotFoundError


OccurrenceLoad: TypeAlias = Tuple[Occurrence, User, Vehicle]


class OccurrenceAggregateRepositoryParams(Protocol):
    occurrence_uuid: str


class OccurrenceAggregateRepository(BaseRepository):
    def aggregate(self, params: OccurrenceAggregateRepositoryParams) -> OccurrenceLoad:
        result: Optional[Row[OccurrenceLoad]] = (
            self.session.query(Occurrence, User, Vehicle)
            .join(User, Occurrence.id_usuario == User.id)
            .join(Vehicle, Occurrence.id_veiculo == Vehicle.id)
            .filter(Occurrence.id_uuid == params.occurrence_uuid)
            .first()
        )

        if not result:
            raise OccurrenceNotFoundError()

        return result.tuple()

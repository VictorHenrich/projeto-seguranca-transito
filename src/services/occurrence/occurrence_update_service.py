from dataclasses import dataclass

from server import App
from models import Vehicle
from patterns.repository import IUpdateRepository
from repositories.occurrence import (
    OccurrenceUpdateRepository,
    OccurrenceUpdateRepositoryParams,
)


@dataclass
class OccurrenceUpdateServiceProps:
    occurrence_uuid: str
    vehicle: Vehicle
    description: str
    obs: str
    address_state: str
    address_city: str
    address_district: str
    address_street: str
    address_number: str


class OccurrenceUpdateService:
    def __init__(
        self,
        occurrence_uuid: str,
        vehicle: Vehicle,
        description: str,
        obs: str,
        address_state: str,
        address_city: str,
        address_district: str,
        address_street: str,
        address_number: str,
    ) -> None:
        self.__props: OccurrenceUpdateServiceProps = OccurrenceUpdateServiceProps(
            occurrence_uuid,
            vehicle,
            description,
            obs,
            address_state,
            address_city,
            address_district,
            address_street,
            address_number,
        )

    def execute(self, props: OccurrenceUpdateServiceProps) -> None:
        with App.databases.create_session() as session:
            update_repository: IUpdateRepository[
                OccurrenceUpdateRepositoryParams, None
            ] = OccurrenceUpdateRepository(session)

            update_repository.update(self.__props)

            session.commit()

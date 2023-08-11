from typing import Protocol

from patterns.repository import BaseRepository, IFindRepository
from models import Occurrence, Vehicle
from .occurrence_find import (
    OccurrenceFindRepository,
    OccurrenceFindRepositoryParams,
)


class OccurrenceUpdateRepositoryParams(Protocol):
    occurrence_uuid: str
    vehicle: Vehicle
    description: str
    address_state: str
    address_city: str
    address_district: str
    address_street: str
    address_number: str


class OccurrenceUpdateRepository(BaseRepository):
    def update(self, params: OccurrenceUpdateRepositoryParams) -> None:
        getting_repository: IFindRepository[
            OccurrenceFindRepositoryParams, Occurrence
        ] = OccurrenceFindRepository(self.session)

        occurrence: Occurrence = getting_repository.find_one(params)

        occurrence.id_veiculo = params.vehicle.id
        occurrence.descricao = params.description
        occurrence.endereco_uf = params.address_state
        occurrence.endereco_cidade = params.address_city
        occurrence.endereco_bairro = params.address_district
        occurrence.endereco_logragouro = params.address_street
        occurrence.endereco_numero = params.address_number

        self.session.add(occurrence)

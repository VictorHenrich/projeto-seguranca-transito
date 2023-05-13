from typing import Protocol
from dataclasses import dataclass

from patterns.repository import BaseRepository, IFindRepository
from models import Occurrence
from .occurrence_find_repository import (
    OccurrenceFindRepository,
    OccurrenceFindRepositoryParams,
)


class OccurrenceUpdateRepositoryParam(Protocol):
    uuid_occurrence: str
    description: str
    obs: str
    address_state: str
    address_city: str
    address_district: str
    address_street: str
    address_number: str
    lat: str
    lon: str


@dataclass
class OccurrenceFindProps:
    uuid_occurrence: str


class OccurrenceUpdateRepository(BaseRepository):
    def update(self, params: OccurrenceUpdateRepositoryParam) -> None:
        getting_repository: IFindRepository[
            OccurrenceFindRepositoryParams, Occurrence
        ] = OccurrenceFindRepository(self.session)

        getting_repository_param: OccurrenceFindRepositoryParams = OccurrenceFindProps(
            uuid_occurrence=params.uuid_occurrence
        )

        occurrence: Occurrence = getting_repository.find_one(getting_repository_param)

        occurrence.descricao = params.description
        occurrence.obs = params.obs
        occurrence.descricao = params.description
        occurrence.obs = params.obs
        occurrence.endereco_uf = params.address_state
        occurrence.endereco_cidade = params.address_city
        occurrence.endereco_bairro = params.address_district
        occurrence.endereco_logragouro = params.address_street
        occurrence.endereco_numero = params.address_number

        self.session.add(occurrence)

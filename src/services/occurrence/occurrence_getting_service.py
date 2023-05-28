from typing import Mapping, Any
from dataclasses import dataclass

from server import App
from patterns.repository import IFindRepository
from models import Occurrence
from repositories.occurrence import (
    OccurrenceFindRepository,
    OccurrenceFindRepositoryParams,
)


@dataclass
class OccurrenceFindProps:
    occurrence_uuid: str


class OccurrenceGettingService:
    def __init__(self, occurrence_uuid: str) -> None:
        self.__props: OccurrenceFindProps = OccurrenceFindProps(occurrence_uuid)

    def execute(self) -> Mapping[str, Any]:
        with App.databases.create_session() as session:
            getting_repository: IFindRepository[
                OccurrenceFindRepositoryParams, Occurrence
            ] = OccurrenceFindRepository(session)

            occurrence: Occurrence = getting_repository.find_one(self.__props)

            return {
                "id_uuid": occurrence.id_uuid,
                "descricao": occurrence.descricao,
                "data_cadastro": occurrence.data_cadastro,
                "endereco_uf": occurrence.endereco_uf,
                "endereco_cidade": occurrence.endereco_cidade,
                "endereco_bairro": occurrence.endereco_bairro,
                "endereco_logradouro": occurrence.endereco_logragouro,
                "endereco_numero": occurrence.endereco_numero,
                "latitude": occurrence.latitude,
                "longitude": occurrence.longitude,
                "status": occurrence.status,
            }

from typing import Collection, Mapping, Any
from dataclasses import dataclass

from server import Databases
from patterns.repository import IFindManyRepository
from models import User, Occurrence
from repositories.occurrence import (
    OccurrenceFindManyRepository,
    OccurrenceFindManyRepositoryParams,
)
from utils.types import DictType


@dataclass
class OccurrenceFindManyProps:
    user: User


class OccurrenceListingService:
    def __init__(self, user: User) -> None:
        self.__props: OccurrenceFindManyProps = OccurrenceFindManyProps(user)

    def execute(self) -> Collection[DictType]:
        with Databases.create_session() as session:
            listing_repository: IFindManyRepository[
                OccurrenceFindManyRepositoryParams, Occurrence
            ] = OccurrenceFindManyRepository(session)

            occurrences: Collection[Occurrence] = listing_repository.find_many(
                self.__props
            )

            return [
                {
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
                for occurrence in occurrences
            ]

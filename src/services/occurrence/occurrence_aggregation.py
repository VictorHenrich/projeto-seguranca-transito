from typing import Collection, Tuple, TypeAlias
from dataclasses import dataclass
from sqlalchemy.orm import Session

from server.database import Databases
from models import User, Occurrence, Vehicle
from patterns.repository import IFindManyRepository
from repositories.occurrence import (
    OccurrenceAggregateRepository,
    OccurrenceAggregateRepositoryParams,
)
from utils.types import DictType

OccurrenceAggregateItemType: TypeAlias = Tuple[Occurrence, Vehicle]


@dataclass
class OccurrenceAggregateProps:
    user: User


class OccurrenceAggregationService:
    def __init__(self, user: User) -> None:
        self.__occurrence_filter: OccurrenceAggregateProps = OccurrenceAggregateProps(
            user
        )

    def __handle_occurrence_data(
        self, occurrence_data: OccurrenceAggregateItemType
    ) -> DictType:
        occurrence, vehicle = occurrence_data

        return {
            "uuid": occurrence.id_uuid,
            "description": occurrence.descricao,
            "lat": occurrence.latitude,
            "lon": occurrence.longitude,
            "status": occurrence.status,
            "created": occurrence.data_cadastro,
            "address": {
                "state": occurrence.endereco_uf,
                "city": occurrence.endereco_cidade,
                "district": occurrence.endereco_bairro,
                "street": occurrence.endereco_logragouro,
                "number": occurrence.endereco_numero,
            },
            "vehicle": {
                "uuid": vehicle.id_uuid,
                "plate": vehicle.placa,
                "renavam": vehicle.renavam,
                "type": vehicle.tipo_veiculo,
                "color": vehicle.cor,
                "brand": vehicle.marca,
                "model": vehicle.modelo,
                "year": vehicle.ano,
                "chassi": vehicle.chassi,
                "have_sefe": vehicle.possui_seguro,
            },
        }

    def __find_occurrences(self, session: Session) -> Collection[DictType]:
        occurrence_aggregate_repo: IFindManyRepository[
            OccurrenceAggregateRepositoryParams, OccurrenceAggregateItemType
        ] = OccurrenceAggregateRepository(session)

        occurrences: Collection[
            OccurrenceAggregateItemType
        ] = occurrence_aggregate_repo.find_many(self.__occurrence_filter)

        return [
            self.__handle_occurrence_data(occurrence_data)
            for occurrence_data in occurrences
        ]

    def execute(self) -> Collection[DictType]:
        with Databases.create_session() as session:
            return self.__find_occurrences(session)

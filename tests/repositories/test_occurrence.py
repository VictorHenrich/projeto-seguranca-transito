from typing import Collection, Tuple
from unittest import TestCase
from unittest.mock import Mock
from pprint import pprint
from datetime import datetime

from .database import database
from src.models import Occurrence, Vehicle
from src.patterns.repository import (
    ICreateRepository,
    IFindRepository,
    IFindManyRepository,
    IUpdateRepository,
)
from src.repositories.occurrence import (
    OccurrenceCreateRepository,
    OccurrenceCreateRepositoryParams,
    OccurrenceFindRepository,
    OccurrenceFindRepositoryParams,
    OccurrenceFindManyRepository,
    OccurrenceFindManyRepositoryParams,
    OccurrenceAggregateRepository,
    OccurrenceAggregateRepositoryParams,
    OccurrenceUpdateRepository,
    OccurrenceUpdateRepositoryParams,
    OccurrenceUpdateStatusRepository,
    OccurrenceUpdateStatusRepositoryParams,
)


class OccurrenceRepositoryCase(TestCase):
    def setUp(self) -> None:
        self.__occurrence_payload: Mock = Mock()

        self.__user_payload: Mock = Mock()

        self.__vehicle_payload: Mock = Mock()

        self.__user_payload.id = 8

        self.__vehicle_payload.id = 1

        self.__occurrence_payload.user = self.__user_payload
        self.__occurrence_payload.vehicle = self.__vehicle_payload
        self.__occurrence_payload.description = "UM ACIDENTE TAL ACONTECEU"
        self.__occurrence_payload.address_state = "SC"
        self.__occurrence_payload.address_city = "CIDADE TAL"
        self.__occurrence_payload.address_district = "BAIRRO TAL"
        self.__occurrence_payload.address_street = "RUAL TAL"
        self.__occurrence_payload.address_number = "S/N"
        self.__occurrence_payload.address_zipcode = "S/N"
        self.__occurrence_payload.lat = "1.00000"
        self.__occurrence_payload.lon = "2.00000"
        self.__occurrence_payload.created = datetime.now()
        self.__occurrence_payload.occurrence_uuid = ""
        self.__occurrence_payload.obs = "ISTO É APENAS UM TESTE"

    def test_create(self) -> None:
        with database.create_session() as session:
            occurrence_repository: ICreateRepository[
                OccurrenceCreateRepositoryParams, Occurrence
            ] = OccurrenceCreateRepository(session)

            occurrence_created: Occurrence = occurrence_repository.create(
                self.__occurrence_payload
            )

            session.commit()

            pprint(f"OCCURRENCE CREATED ====> {occurrence_created}")

            self.assertTrue(occurrence_created)

    def test_find(self) -> None:
        with database.create_session() as session:
            occurrence_repository: IFindRepository[
                OccurrenceFindRepositoryParams, Occurrence
            ] = OccurrenceFindRepository(session)

            occurrence_finded: Occurrence = occurrence_repository.find_one(
                self.__occurrence_payload
            )

            pprint(f"OCCURRENCE FINDED ====> {occurrence_finded}")

            self.assertTrue(occurrence_finded)

    def test_find_many(self) -> None:
        with database.create_session() as session:
            occurrence_repository: IFindManyRepository[
                OccurrenceFindManyRepositoryParams, Occurrence
            ] = OccurrenceFindManyRepository(session)

            occurrences: Collection[Occurrence] = occurrence_repository.find_many(
                self.__occurrence_payload
            )

            pprint(f"OCCURRENCES FINDED ====> {occurrences}")

            self.assertTrue(occurrences)

    def test_aggregate(self) -> None:
        with database.create_session() as session:
            occurrence_repository: IFindManyRepository[
                OccurrenceAggregateRepositoryParams, Tuple[Occurrence, Vehicle]
            ] = OccurrenceAggregateRepository(session)

            occurrence_aggregated: Collection[
                Tuple[Occurrence, Vehicle]
            ] = occurrence_repository.find_many(self.__occurrence_payload)

            pprint(f"OCCURRENCE FINDED ====> {occurrence_aggregated}")

            self.assertTrue(occurrence_aggregated)

    def test_update(self) -> None:
        with database.create_session() as session:
            occurrence_repository: IUpdateRepository[
                OccurrenceUpdateRepositoryParams, None
            ] = OccurrenceUpdateRepository(session)

            occurrence_repository.update(self.__occurrence_payload)

            pprint("OCCURRENCE UPDATED")

    def test_update_status(self) -> None:
        with database.create_session() as session:
            occurrence_update_params: Mock = Mock()

            occurrence_update_params.occurrence = self.__occurrence_payload
            occurrence_update_params.status = "ANDAMENTO"

            occurrence_repository: IUpdateRepository[
                OccurrenceUpdateStatusRepositoryParams, None
            ] = OccurrenceUpdateStatusRepository(session)

            occurrence_repository.update(occurrence_update_params)

from sqlalchemy.orm import Session
from start import app
from patterns import CrudRepository
from models import TipoOcorrencia
from exceptions import OccurrenceTypeNotFoundError
from .interfaces import IOccurrenceTypeRegistration, IOccurrenceTypeLocation, IOccurrenceTypeListing



class CrudOccurrenceTypeRepository(CrudRepository[TipoOcorrencia]):
    def __get_occurrence_type(self, session: Session, location: IOccurrenceTypeLocation) -> TipoOcorrencia:
        occurrence_type: TipoOcorrencia = \
            session\
                .query(TipoOcorrencia)\
                .filter(
                    TipoOcorrencia.id_uuid == location.uuid
                )\
                .first()

        if not occurrence_type:
            raise OccurrenceTypeNotFoundError()

    def create(self, data: IOccurrenceTypeRegistration) -> None:
        with app.databases.create_session() as session:
            occurrence_type: TipoOcorrencia = TipoOcorrencia()

            occurrence_type.id_nivel = data.level.id
            occurrence_type.descricao = data.description
            occurrence_type.instrucao = data.instruction

            session.add(occurrence_type)
            session.commit()

    def update(self, location: IOccurrenceTypeLocation, data: IOccurrenceTypeRegistration) -> None:
        with app.databases.create_session() as session:
            occurrence_type: TipoOcorrencia = self.__get_occurrence_type(
                session,
                location
            )

            occurrence_type.id_nivel = data.level.id
            occurrence_type.descricao = data.description
            occurrence_type.instrucao = data.instruction

            session.add(occurrence_type)
            session.commit()

    def delete(self, location: IOccurrenceTypeLocation) -> None:
        with app.databases.create_session() as session:
            occurrence_type: TipoOcorrencia = self.__get_occurrence_type(
                session,
                location
            )

            session.delete(occurrence_type)
            session.commit()

    def load(self, location: IOccurrenceTypeLocation) -> TipoOcorrencia:
        with app.databases.create_session() as session:
            occurrence_type: TipoOcorrencia = self.__get_occurrence_type(
                session,
                location
            )

            return occurrence_type

    def fetch(self, list_location: IOccurrenceTypeListing) -> list[TipoOcorrencia]:
        with app.databases.create_session() as session:
            occurrences_types_list: list[TipoOcorrencia] = \
                session\
                    .query(TipoOcorrencia)\
                    .filter(
                        TipoOcorrencia.id_departamento == list_location.departament.id
                    )\
                    .all()

            return occurrences_types_list
from sqlalchemy.orm import Session

from start import app
from patterns import CrudRepository
from models import Ocorrencia, Departamento
from exceptions import OccurrenceNotFoundError
from .interfaces import IOccurrenceRegistration, IOccurrenceLocation



class CrudOccurrenceRepository(CrudRepository[Ocorrencia]):
    def __get_occurrence(
        self, 
        session: Session, 
        location: IOccurrenceLocation
    ) -> Ocorrencia:
        occurrence: Ocorrencia = \
            session\
                .query(Ocorrencia)\
                .filter(
                    Ocorrencia.id_uuid == location.uuid,
                    Ocorrencia.id_departamento == location.departament.id
                )\
                .first()

        if not occurrence:
            raise OccurrenceNotFoundError()

        return occurrence

    def create(self, data: IOccurrenceRegistration) -> None:
        with app.databases.create_session() as session:
            occurrence: Ocorrencia = Ocorrencia()

            occurrence: Ocorrencia = Ocorrencia()

            occurrence.id_departamento = data.departament.id
            occurrence.id_usuario = data.user.id
            occurrence.descricao = data.description
            occurrence.obs = data.obs
            
            session.add(occurrence)
            session.commit()

    def update(self, location: IOccurrenceLocation, data: IOccurrenceRegistration) -> None:
        with app.databases.create_session() as session:
            occurrence: Ocorrencia = self.__get_occurrence(session, location)

            occurrence.descricao = data.description
            occurrence.obs = data.obs

            session.add(occurrence)
            session.commit()

    def delete(self, location: IOccurrenceLocation) -> None:
        with app.databases.create_session() as session:
            occurrence: Ocorrencia = self.__get_occurrence(session, location)

            session.delete(occurrence)
            session.commit()

    def load(self, location: IOccurrenceLocation) -> Ocorrencia:
        with app.databases.create_session() as session:
            occurrence: Ocorrencia =  self.__get_occurrence(session, location)

            return occurrence

    def fetch(self, location: IOccurrenceLocation) -> list[Ocorrencia]:
        with app.databases.create_session() as session:
            occurrences_list: list[Ocorrencia] = \
                session\
                    .query(Ocorrencia)\
                    .filter(
                        Ocorrencia.id_departamento == location.departament.id
                    )\
                    .all()

            return occurrences_list
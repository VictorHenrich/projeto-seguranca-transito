from typing import Optional

from start import server
from services.database import Database
from patterns.utils import Repository
from patterns.ocorrencia import OccurrenceRegistration
from models import Ocorrencia, Departamento, Usuario
from exceptions import OccurrenceNotFoundError
from repositories import UserRepository


db: Database = server.databases.get_database()


class OccurrenceRepository(Repository[Ocorrencia]):
    @staticmethod
    def create(
        departament: Departamento,
        data: OccurrenceRegistration
    ) -> None:
        with db.create_session() as session:
            user: Usuario = \
                session\
                    .query(Usuario)\
                    .filter(Usuario.id_uuid == data.uuid_usuario)

            occurrence: Ocorrencia = Ocorrencia()

            occurrence.id_departamento = departament.id
            occurrence.id_usuario = user.id
            occurrence.descricao = data.descricao
            occurrence.obs = data.obs
            
            session.add(occurrence)
            session.commit()

    @staticmethod
    def update(
        uuid: str,
        departament: Departamento, 
        data: OccurrenceRegistration
    ) -> None:
        with db.create_session() as session:
            occurrence: Ocorrencia = \
                session\
                    .query(Ocorrencia)\
                    .filter(
                        Ocorrencia.id_departamento == departament.id,
                        Ocorrencia.id_uuid == uuid
                    )\
                    .first()

            if not occurrence:
                raise OccurrenceNotFoundError()


            occurrence.descricao = data.descricao
            occurrence.obs = data.obs

            session.add(occurrence)
            session.commit()

    @staticmethod
    def delete(
        uuid: str,
        departament: Departamento, 
    ) -> None:
        with db.create_session() as session:
            occurrence: Optional[Ocorrencia] = \
                session\
                    .query(Ocorrencia)\
                    .filter(
                        Ocorrencia.id_departamento == departament.id,
                        Ocorrencia.id_uuid == uuid
                    )\
                    .first()

            if not occurrence:
                raise OccurrenceNotFoundError()

            session.delete(occurrence)
            session.commit()

    @staticmethod
    def fetch(departament: Departamento) -> list[Ocorrencia]:
        with db.create_session() as session:
            occurrences: list[Ocorrencia] = \
                session\
                    .query(Ocorrencia)\
                    .filter(
                        Ocorrencia.id_departamento == departament.id
                    )\
                    .all()

            return occurrences

    @staticmethod
    def get(
        uuid: str,
        departament: Departamento, 
    ) -> Ocorrencia:
        with db.create_session() as session:
            occurrence: Optional[Ocorrencia] = \
                session\
                    .query(Ocorrencia)\
                    .filter(
                        Ocorrencia.id_departamento == departament.id,
                        Ocorrencia.id_uuid == uuid
                    )\
                    .first()

            if not occurrence:
                raise OccurrenceNotFoundError()

            return occurrence

            

            

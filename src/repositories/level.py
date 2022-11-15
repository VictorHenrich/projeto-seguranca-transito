from start import server
from services.database import Database
from patterns.utils import Repository
from patterns.nivel import LevelRegistration
from models import Nivel, Departamento
from exceptions import LevelNotFoundError



db: Database = server.databases.get_database()


class LevelRepository(Repository[Nivel]):
    @staticmethod
    def fetch(departament: Departamento) -> list[Nivel]:
        with db.create_session() as session:
            levels: list[Nivel] = \
                session\
                    .query(Nivel)\
                    .join(Departamento, Nivel.id_departamento == Departamento.id)\
                    .filter(Departamento.id == departament.id)\
                    .all()

            return levels

    @staticmethod
    def create(departament: Departamento, data: LevelRegistration) -> None:
        with db.create_session() as session:
            level: Nivel = Nivel()

            level.id_departamento = departament.id
            level.descricao = data.descricao
            level.nivel = data.nivel
            level.obs - data.obs
            
            session.add(level)
            session.commit()

    @staticmethod
    def update(uuid: str, departament: Departamento, data: LevelRegistration) -> None:
        with db.create_session() as session:
            level: Nivel = \
                session\
                    .query(Nivel)\
                    .filter(
                        Departamento.id == departament.id,
                        Nivel.uuid == uuid
                    )\
                    .first()

            if not level:
                raise LevelNotFoundError()

            level.descricao = data.descricao
            level.nivel = data.nivel
            level.obs - data.obs
            
            session.add(level)
            session.commit()
            
    @staticmethod
    def delete(uuid: str, departament: Departamento) -> None:
        with db.create_session() as session:
            level: Nivel = \
                session\
                    .query(Nivel)\
                    .filter(
                        Departamento.id == departament.id,
                        Nivel.uuid == uuid
                    )\
                    .first()

            if not level:
                raise LevelNotFoundError()

            session.delete(level)
            session.commit()

    @staticmethod
    def get(uuid: str, departament: Departamento) -> Nivel:
        with db.create_session() as session:
            level: Nivel = \
                session\
                    .query(Nivel)\
                    .filter(
                        Departamento.id == departament.id,
                        Nivel.uuid == uuid
                    )\
                    .all()

            if not level:
                raise LevelNotFoundError()

            return level
        
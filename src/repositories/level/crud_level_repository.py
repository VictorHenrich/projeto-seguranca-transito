from start import app
from sqlalchemy.orm import Session
from patterns import CrudRepository
from exceptions import LevelNotFoundError
from .interfaces import LevelWriteData, LevelLocationData
from models import Nivel, Departamento



class CrudLevelRepository(CrudRepository[Nivel]):
    def __get_level(self, session: Session, location: LevelLocationData) -> Nivel:
        with app.databases.create_session() as session:
            level: Nivel = \
                session\
                    .query(Nivel)\
                    .filter(
                        Nivel.id_uuid == location.uuid,
                        Nivel.id_departamento == location.departament.id
                    )\
                    .first()

            if not level:
                raise LevelNotFoundError()

    def create(self, departament: Departamento, data: LevelWriteData) -> None:
        with app.databases.create_session() as session:
            level: Nivel = Nivel()

            level.id_departamento = departament.id
            level.descricao = data.description
            level.nivel = data.level
            level.obs = data.obs

            session.add(level)
            session.commit()

    def update(self, location: LevelLocationData, data: LevelWriteData) -> None:
        with app.databases.create_session() as session:
            level: Nivel = self.__get_level(session, location)

            level.descricao = data.description
            level.nivel = data.level
            level.obs = data.obs
            
            session.add(level)
            session.commit()

    def delete(self, location: LevelLocationData) -> None:
        with app.databases.create_session() as session:
            level: Nivel = self.__get_level(session, location)

            session.delete(level)
            session.commit()

    def load(self, location: LevelLocationData) -> Nivel:
        with app.databases.create_session() as session:
            level: Nivel = self.__get_level(session, location)

            return level

    def fetch(self, location: LevelLocationData) -> list[Nivel]:
        with app.databases.create_session() as session:
            levels_list: list[Nivel] = \
                session\
                    .query(Nivel)\
                    .filter(
                        Nivel.id_departamento == location.departament.id
                    )\
                    .all()

            return levels_list
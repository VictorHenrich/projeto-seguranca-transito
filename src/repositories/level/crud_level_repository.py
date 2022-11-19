from start import app
from sqlalchemy.orm import Session
from patterns import CrudRepository
from exceptions import LevelNotFoundError
from .interfaces import ILevelRegistration, ILevelLocation
from models import Nivel



class CrudLevelRepository(CrudRepository[Nivel]):
    def __get_level(self, session: Session, location: ILevelLocation) -> Nivel:
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

    def create(self, data: ILevelRegistration) -> None:
        with app.databases.create_session() as session:
            level: Nivel = Nivel()

            level.id_departamento = data.departament.id
            level.descricao = data.description
            level.nivel = data.level
            level.obs = data.obs

            session.add(level)
            session.commit()

    def update(self, location: ILevelLocation, data: ILevelRegistration) -> None:
        with app.databases.create_session() as session:
            level: Nivel = self.__get_level(session, location)

            level.descricao = data.description
            level.nivel = data.level
            level.obs = data.obs
            
            session.add(level)
            session.commit()

    def delete(self, location: ILevelLocation) -> None:
        with app.databases.create_session() as session:
            level: Nivel = self.__get_level(session, location)

            session.delete(level)
            session.commit()

    def load(self, location: ILevelLocation) -> Nivel:
        with app.databases.create_session() as session:
            level: Nivel = self.__get_level(session, location)

            return level

    def fetch(self, location: ILevelLocation) -> list[Nivel]:
        with app.databases.create_session() as session:
            levels_list: list[Nivel] = \
                session\
                    .query(Nivel)\
                    .filter(
                        Nivel.id_departamento == location.departament.id
                    )\
                    .all()

            return levels_list
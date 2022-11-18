from sqlalchemy.orm import Session

from start import app
from patterns import CrudRepository
from exceptions import UserNotFoundError
from models import Usuario
from .interfaces import UserWriteData, UserLocationData



class CrudUserRepository(CrudRepository[Usuario]):
    def __get_user(self, session: Session, location: UserLocationData) -> Usuario:
        user: Usuario = \
            session\
                .query(Usuario)\
                .filter(Usuario.id_uuid == location.uuid)\
                .first()

        if not user:
            raise UserNotFoundError()

    def create(self, data: UserWriteData) -> None:
        with app.databases.create_session() as session:
            user: Usuario = Usuario()

            user.nome = data.name
            user.email = data.email
            user.cpf = data.document
            user.senha = data.password
            user.data_nascimento = data.date_birth

            session.add(user)
            session.commit()

    def update(self, location: UserLocationData, data: UserWriteData) -> None:
        with app.databases.create_session() as session:
            user: Usuario = self.__get_user(session, location)

            user.nome = data.name
            user.email = data.email
            user.cpf = data.document
            user.senha = data.password
            user.data_nascimento = data.date_birth

            session.add(user)
            session.commit()

    def delete(self, location: UserLocationData) -> None:
        with app.databases.create_session() as session:
            user: Usuario = self.__get_user(session, location)

            session.delete(user)
            session.commit()

    def load(self, location: UserLocationData) -> Usuario:
        with app.databases.create_session() as session:
            user: Usuario = self.__get_user(session, location)

            return user

    def fetch(self) -> list[Usuario]:
        with app.databases.create_session() as session:
            users_list: list[Usuario] = \
                session\
                    .query(Usuario)\
                    .all()

            return users_list
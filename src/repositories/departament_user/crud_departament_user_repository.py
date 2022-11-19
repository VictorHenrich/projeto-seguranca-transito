from typing import Optional
from sqlalchemy.orm import Session

from start import app
from patterns import CrudRepository
from models import UsuarioDepartamento, Departamento
from exceptions import UserNotFoundError
from .interfaces import IUserDepartamentRegistration, IUserDepartamentLocation




class CrudDepartamentUserRepository(CrudRepository[UsuarioDepartamento]):

    def __get_user(
        self,
        session: Session,
        location: IUserDepartamentLocation
    ) -> UsuarioDepartamento:
        user: Optional[UsuarioDepartamento] = \
            session\
                .query(UsuarioDepartamento)\
                .filter(
                    UsuarioDepartamento.id_uuid == location.uuid,
                    UsuarioDepartamento.id_departamento == location.departament.id
                )\
                .first()

        if not user:
            raise UserNotFoundError()

        return user
            
    def load(self, location: IUserDepartamentLocation) -> UsuarioDepartamento:
        with app.databases.create_session() as session:
            user: UsuarioDepartamento = self.__get_user(session, location)

            return user

    def fetch(self, location: IUserDepartamentLocation) -> list[UsuarioDepartamento]:
        with app.databases.create_session() as session:
            users_list: list[UsuarioDepartamento] = \
                session\
                    .query(UsuarioDepartamento)\
                    .filter(UsuarioDepartamento.id_departamento == location.departament.id)\
                    .all()

            return users_list

    def create(self, data: IUserDepartamentRegistration) -> None:
        with app.databases.create_session() as session:
            user: UsuarioDepartamento = UsuarioDepartamento()

            user.nome = data.name
            user.acesso = data.user
            user.cargo = data.office
            user.senha = data.password
            user.id_departamento = data.departament.id
            
            session.add(user)
            session.commit()

    def update(self, location: IUserDepartamentLocation, data: IUserDepartamentRegistration) -> None:
        with app.databases.create_session() as session:
            user: UsuarioDepartamento = self.__get_user(session, location)

            user.acesso = data.user
            user.nome = data.name
            user.cargo = data.office
            user.senha = data.password

            if type(data.departament) is Departamento:
                user.id_departamento = data.departament.id

            session.add(user)
            session.commit()

    def delete(self, location: IUserDepartamentLocation) -> None:
        with app.databases.create_session() as session:
            user: UsuarioDepartamento = self.__get_user(session, location)

            session.delete(user)
            session.commit()

    
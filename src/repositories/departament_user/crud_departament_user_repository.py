from typing import Optional
from sqlalchemy.orm import Session

from start import app
from patterns import CrudRepository
from models import UsuarioDepartamento, Departamento
from exceptions import UserNotFoundError
from .interfaces import UserDepartamentWriteData, UserDepartamentLocationData




class CrudDepartamentUserRepository(CrudRepository[UsuarioDepartamento]):

    def __get_user(
        self,
        session: Session,
        location: UserDepartamentLocationData
    ) -> UsuarioDepartamento:
        user: Optional[UsuarioDepartamento] = \
            session\
                .query(UsuarioDepartamento)\
                .filter(
                    UsuarioDepartamento.id_uuid == location.uuid,
                    UsuarioDepartamento.id_departamento == location.departament_id
                )\
                .first()

        if not user:
            raise UserNotFoundError()

        return user
            
    def load(self, location: UserDepartamentLocationData) -> UsuarioDepartamento:
        with app.databases.create_session() as session:
            user: UsuarioDepartamento = self.__get_user(session, location)

            return user

    def fetch(self, location: UserDepartamentLocationData) -> list[UsuarioDepartamento]:
        with app.databases.create_session() as session:
            users_list: list[UsuarioDepartamento] = \
                session\
                    .query(UsuarioDepartamento)\
                    .filter(UsuarioDepartamento.id_departamento == location.departament.id)\
                    .all()

            return users_list

    def create(self, departament: Departamento, data: UserDepartamentWriteData) -> None:
        with app.databases.create_session() as session:
            user: UsuarioDepartamento = UsuarioDepartamento()

            user.nome = data.name
            user.acesso = data.user
            user.cargo = data.office
            user.senha = data.password
            user.id_departamento = departament.id
            
            session.add(user)
            session.commit()

    def update(self, location: UserDepartamentLocationData, data: UserDepartamentWriteData) -> None:
        with app.databases.create_session() as session:
            user: UsuarioDepartamento = self.__get_user(session, location)

            user.acesso = data.user
            user.nome = data.name
            user.cargo = data.office
            user.senha = data.password

            session.add(user)
            session.commit()

    def delete(self, location: UserDepartamentLocationData) -> None:
        with app.databases.create_session() as session:
            user: UsuarioDepartamento = self.__get_user(session, location)

            session.delete(user)
            session.commit()

    
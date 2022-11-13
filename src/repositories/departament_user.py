from typing import Optional

from start import server
from services.database import Database
from patterns.utils import Repository
from models import UsuarioDepartamento
from exceptions import UserNotFoundError



db: Database = server.databases.get_database()


class DepartamentUserRepository(Repository[UsuarioDepartamento]):
    @staticmethod
    def create(
        nome: str,
        usuario: str,
        cargo: str,
        senha: str,
        id_departamento: int 
    ) -> None:
        with db.create_session() as session:
            usuario_: UsuarioDepartamento = UsuarioDepartamento()

            usuario_.nome = nome
            usuario_.acesso = usuario
            usuario_.cargo = cargo
            usuario_.senha = senha
            usuario_.id_departamento = id_departamento
            
            session.add(usuario_)
            session.commit()

    @staticmethod
    def update(
        uuid: str,
        nome: str,
        usuario: str,
        cargo: str,
        senha: str,
    ) -> None:
        with db.create_session() as session:
            usuario: Optional[UsuarioDepartamento] = \
                session\
                    .query(UsuarioDepartamento)\
                    .filter(UsuarioDepartamento.id_uuid == uuid)\
                    .first()

            if not usuario:
                raise UserNotFoundError()

            usuario.acesso = usuario
            usuario.nome = nome
            usuario.cargo = cargo
            usuario.senha = senha

    @staticmethod
    def delete(uuid: str) -> None:
        with db.create_session() as session:
            usuario: UsuarioDepartamento = \
                session\
                    .query(UsuarioDepartamento)\
                    .filter(
                        UsuarioDepartamento.id_uuid == uuid
                    )\
                    .first()

            if not usuario:
                raise UserNotFoundError()

            session.delete(usuario)
            session.commit()

    @staticmethod
    def get(
        usuario: str,
        senha: str,
        id_departamento: int
    ) -> UsuarioDepartamento:
        with db.create_session() as session:
            usuario_: UsuarioDepartamento = \
                session\
                    .query(UsuarioDepartamento)\
                    .filter(
                        UsuarioDepartamento.acesso == usuario,
                        UsuarioDepartamento.senha == senha,
                        UsuarioDepartamento.id_departamento == id_departamento
                    )\
                    .first()

            if not usuario_:
                raise UserNotFoundError()

            return usuario_

    @staticmethod
    def list(id_departamento: int) -> list[UsuarioDepartamento]:
        with db.create_session() as session:
            usuarios: list[UsuarioDepartamento] = \
                session\
                    .query(UsuarioDepartamento)\
                    .filter(UsuarioDepartamento.id_departamento == id_departamento)\
                    .all()

            return usuarios
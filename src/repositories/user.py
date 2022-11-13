from typing import Optional
from sqlalchemy import func
from start import server
from services.database import Database
from patterns.utils import Repository
from models import Usuario
from exceptions import UserNotFoundError



db: Database = server.databases.get_database()


class UserRepository(Repository[Usuario]):
    @staticmethod
    def create( 
        nome: str,
        email: str,
        cpf: str,
        senha: str,
        data_nascimento: Optional[str],
    ) -> None:
        with db.create_session() as session:
            usuario: Usuario = Usuario()

            usuario.nome = nome
            usuario.email = email
            usuario.cpf = cpf
            usuario.senha = senha
            usuario.data_nascimento = data_nascimento

            session.add(usuario)
            session.commit()

    @staticmethod
    def update(
        id: int,
        nome: str,
        email: str,
        cpf: str,
        senha: str,
        data_nascimento: Optional[str],
    ) -> None:
        with db.create_session() as session:
            usuario: Usuario = \
                session\
                    .query(Usuario)\
                    .filter(Usuario.id == id)\
                    .first()

            if not usuario:
                raise UserNotFoundError()

            usuario.nome = nome
            usuario.email = email
            usuario.cpf = cpf
            usuario.data_nascimento = data_nascimento
            usuario.senha = senha

            session.add(usuario)
            session.commit()
    
    @staticmethod
    def delete(id: int) -> None:
        with db.create_session() as session:
            usuario: Usuario = \
                    session\
                        .query(Usuario)\
                        .filter(Usuario.id == id)\
                        .first()

            if not usuario:
                raise UserNotFoundError()

            session.delete(usuario)
            session.commit()

    @staticmethod
    def get(
        email: str,
        senha: str
    ) -> Usuario:
        with db.create_session() as session:
            usuario: Usuario = \
                    session\
                        .query(Usuario)\
                        .filter(
                            func.upper(Usuario.email) == email.upper(),
                            Usuario.senha == senha
                        )\
                        .first()

        if not usuario:
            raise UserNotFoundError()

        return usuario

            
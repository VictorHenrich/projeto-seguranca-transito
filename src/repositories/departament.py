from typing import Optional

from start import server
from services.database import Database
from patterns.utils import Repository
from models import Departamento
from exceptions import DepartamentNotFoundError



db: Database = server.databases.get_database()


class DepartamentRepository(Repository[Departamento]):
    @staticmethod
    def get(acesso: str) -> Departamento:
        with db.create_session() as session:
            departamento: Departamento = \
                session\
                    .query(Departamento)\
                    .filter(Departamento.acesso == acesso)\
                    .first()

            if not departamento:
                raise DepartamentNotFoundError()

            return departamento
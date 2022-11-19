from start import app
from patterns import CrudRepository
from models import Departamento
from exceptions import DepartamentNotFoundError
from .interfaces import IDepartamentLocation


class CrudDepartamentRepository(CrudRepository[Departamento]):
    def load(self, location: IDepartamentLocation) -> Departamento:
        with app.databases.create_session() as session:
            departament: Departamento = \
                session\
                    .query(Departamento)\
                    .filter(
                        Departamento.id_uuid == location.uuid
                    )\
                    .first()

            if not departament:
                raise DepartamentNotFoundError()

            return departament
from typing import List
from dataclasses import dataclass

from start import app
from patterns.repository import IFindManyRepository
from repositories.agent import (
    AgentFindManyRepository,
    AgentFindManyRepositoryParams,
)
from models import UsuarioDepartamento, Departamento


@dataclass
class AgentFindManyProps:
    departament: Departamento


class AgentListingService:
    def execute(self, departament: Departamento) -> List[UsuarioDepartamento]:

        with app.databases.create_session() as session:
            listing_repository_param: AgentFindManyRepositoryParams = (
                AgentFindManyProps(departament=departament)
            )

            listing_repository: IFindManyRepository[
                AgentFindManyRepositoryParams, UsuarioDepartamento
            ] = AgentFindManyRepository(session)

            users: List[UsuarioDepartamento] = listing_repository.list(
                listing_repository_param
            )

            return users

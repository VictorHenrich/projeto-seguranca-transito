from typing import Sequence
from unittest import TestCase
from unittest.mock import Mock

from ..util import TestUtil

TestUtil.load_modules("C:\\projetos\\pessoais\\projeto-seguranca-transito-backend\\src")


from src.start.application import App
from src.models.agent import Agent
from src.repositories.agent import (
    AgentAuthRepository,
    AgentAuthRepositoryParams,
    AgentCreateRepository,
    AgentCreateRepositoryParams,
    AgentUpdateRepository,
    AgentUpdateRepositoryParams,
    AgentDeleteRepository,
    AgentDeleteRepositoryParams,
    AgentFindRepository,
    AgentFindRepositoryParams,
    AgentFindManyRepository,
    AgentFindManyRepositoryParams,
)
from src.patterns.repository import (
    IAuthRepository,
    ICreateRepository,
    IDeleteRepository,
    IFindRepository,
    IFindManyRepository,
    IUpdateRepository,
)


class TestAgentRepository(TestCase):
    def test_agent_auth(self) -> None:
        agent_auth_params: Mock = Mock()

        agent_auth_params.user = "victor.henrich"
        agent_auth_params.password = "1234"
        agent_auth_params.departament_access = "T"

        with App.databases.create_session() as session:
            agent_auth_repository: IAuthRepository[
                AgentAuthRepositoryParams, Agent
            ] = AgentAuthRepository(session)

            agent: Agent = agent_auth_repository.auth(agent_auth_params)

            self.assertIsNotNone(agent)

    def test_agent_create(self) -> None:
        departament: Mock = Mock()

        departament.id = 1

        agent_create_params: Mock = Mock()

        agent_create_params.departament = departament
        agent_create_params.name = "Rodrigo da silva"
        agent_create_params.access = "rodrigo.silva"
        agent_create_params.password = "1234"
        agent_create_params.position = "Gerente"

        with App.databases.create_session() as session:
            agent_create_repository: ICreateRepository[
                AgentCreateRepositoryParams, None
            ] = AgentCreateRepository(session)

            agent_create_repository.create(agent_create_params)

            session.commit()

    def test_agent_update(self) -> None:
        departament: Mock = Mock()

        departament.id = 1

        agent_update_params: Mock = Mock()

        agent_update_params.departament = departament
        agent_update_params.agent_uuid = "fa6c265e-dfe9-4e29-b2d4-6fe2626100a5"
        agent_update_params.name = "Nome alterado"
        agent_update_params.access = "rodrigo.silva"
        agent_update_params.password = "1234"
        agent_update_params.position = "nada"

        with App.databases.create_session() as session:
            agent_update_repository: IUpdateRepository[
                AgentUpdateRepositoryParams, None
            ] = AgentUpdateRepository(session)

            agent_update_repository.update(agent_update_params)

            session.commit()

    def test_agent_delete(self) -> None:
        departament: Mock = Mock()

        departament.id = 1

        agent_delete_params: Mock = Mock()

        agent_delete_params.departament = departament
        agent_delete_params.agent_uuid = "fa6c265e-dfe9-4e29-b2d4-6fe2626100a5"

        with App.databases.create_session() as session:
            agent_delete_repository: IDeleteRepository[
                AgentDeleteRepositoryParams, None
            ] = AgentDeleteRepository(session)

            agent_delete_repository.delete(agent_delete_params)

            session.commit()

    def test_agent_find(self) -> None:
        departament: Mock = Mock()

        departament.id = 1

        agent_find_params: Mock = Mock()

        agent_find_params.departament = departament
        agent_find_params.agent_uuid = "60f64f08-9dd8-41ee-b2af-fccc17bc7765"

        with App.databases.create_session() as session:
            agent_find_repository: IFindRepository[
                AgentFindRepositoryParams, Agent
            ] = AgentFindRepository(session)

            agent: Agent = agent_find_repository.find_one(agent_find_params)

            self.assertIsNotNone(agent)

    def test_agent_find_many(self) -> None:
        departament: Mock = Mock()

        departament.id = 1

        agent_find_many_params: Mock = Mock()

        agent_find_many_params.departament = departament

        with App.databases.create_session() as session:
            agent_find_many_repository: IFindManyRepository[
                AgentFindManyRepositoryParams, Agent
            ] = AgentFindManyRepository(session)

            agents: Sequence[Agent] = agent_find_many_repository.find_many(
                agent_find_many_params
            )

            self.assertTrue(agents)

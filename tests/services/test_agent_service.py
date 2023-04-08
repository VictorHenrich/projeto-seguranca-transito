from typing import List
from unittest import TestCase
from unittest.mock import Mock

from ..util import TestUtil

TestUtil.load_modules()

import src.start.application
from src.patterns.service import IService
from src.models import Agent
from src.services.agent import (
    AgentCreationService,
    AgentCreationServiceProps,
    AgentUpdateService,
    AgentUpdateServiceProps,
    AgentExclusionService,
    AgentExclusionServiceProps,
    AgentFindingService,
    AgentFindingServiceProps,
    AgentsFetchingService,
    AgentsFetchingServiceProps,
    AgentAuthorizationService,
    AgentAuthorizationServiceProps,
)


class TestAgentService(TestCase):
    def test_creation_agent(self) -> None:
        agent_creation_props: Mock = Mock()

        departament: Mock = Mock()

        departament.id = 1

        agent_creation_props.departament = departament
        agent_creation_props.name = "Usuário teste"
        agent_creation_props.access = "teste"
        agent_creation_props.password = "1234"
        agent_creation_props.position = "TESTE"

        agent_creation_service: IService[
            AgentCreationServiceProps, None
        ] = AgentCreationService()

        agent_creation_service.execute(agent_creation_props)

    def test_update_agent(self) -> None:
        agent_update_props: Mock = Mock()

        departament: Mock = Mock()

        departament.id = 1

        agent_update_props.agent_uuid = "8b19abfc-94b2-4494-92e9-ae5fcf79add6"
        agent_update_props.departament = departament
        agent_update_props.name = "Nome Alterado"
        agent_update_props.access = "teste"
        agent_update_props.password = "1234"
        agent_update_props.position = "funcionário publico"

        agent_update_service: IService[
            AgentUpdateServiceProps, None
        ] = AgentUpdateService()

        agent_update_service.execute(agent_update_props)

    def test_exclusion_agent(self) -> None:
        agent_exclusion_props: Mock = Mock()

        departament: Mock = Mock()

        departament.id = 1

        agent_exclusion_props.agent_uuid = "8b19abfc-94b2-4494-92e9-ae5fcf79add6"
        agent_exclusion_props.departament = departament

        agent_exclusion_service: IService[
            AgentExclusionServiceProps, None
        ] = AgentExclusionService()

        agent_exclusion_service.execute(agent_exclusion_props)

    def test_finding_agent(self) -> None:
        agent_finding_props: Mock = Mock()

        departament: Mock = Mock()

        departament.id = 1

        agent_finding_props.agent_uuid = "d9f848e2-113b-4c2e-8407-a7cb41b364fa"
        agent_finding_props.departament = departament

        agent_finding_service: IService[
            AgentFindingServiceProps, Agent
        ] = AgentFindingService()

        agent: Agent = agent_finding_service.execute(agent_finding_props)

        self.assertTrue(agent)

    def test_fetching_agents(self) -> None:
        agent_fetching_props: Mock = Mock()

        departament: Mock = Mock()

        departament.id = 1

        agent_fetching_props.departament = departament

        agent_fetching_service: IService[
            AgentsFetchingServiceProps, List[Agent]
        ] = AgentsFetchingService()

        agents: List[Agent] = agent_fetching_service.execute(agent_fetching_props)

        self.assertTrue(agents)

    def test_auth_agent(self) -> None:
        agent_auth_props: Mock = Mock()

        agent_auth_props.departament_access = "T"
        agent_auth_props.user = "victor.henrich"
        agent_auth_props.password = "1234"

        agent_auth_service: IService[
            AgentAuthorizationServiceProps, str
        ] = AgentAuthorizationService()

        token: str = agent_auth_service.execute(agent_auth_props)

        self.assertTrue(token)

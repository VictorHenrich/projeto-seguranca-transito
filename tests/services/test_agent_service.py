from typing import List
from unittest import TestCase
from unittest.mock import Mock

from ..util import TestUtil

TestUtil.load_modules()


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
        agent_creation_props.name = ""
        agent_creation_props.access = ""
        agent_creation_props.password = ""
        agent_creation_props.position = ""

        agent_creation_service: IService[
            AgentCreationServiceProps, None
        ] = AgentCreationService()

        agent_creation_service.execute(agent_creation_props)

    def test_update_agent(self) -> None:
        agent_update_props: Mock = Mock()

        departament: Mock = Mock()

        departament.id = 1

        agent_update_props.agent_uuid = ""
        agent_update_props.departament = departament
        agent_update_props.name = ""
        agent_update_props.access = ""
        agent_update_props.password = ""
        agent_update_props.position = ""

        agent_update_service: IService[
            AgentUpdateServiceProps, None
        ] = AgentUpdateService()

        agent_update_service.execute(agent_update_props)

    def test_exclusion_agent(self) -> None:
        agent_exclusion_props: Mock = Mock()

        departament: Mock = Mock()

        departament.id = 1

        agent_exclusion_props.agent_uuid = ""

        agent_exclusion_service: IService[
            AgentExclusionServiceProps, None
        ] = AgentExclusionService()

        agent_exclusion_service.execute(agent_exclusion_props)

    def test_finding_agent(self) -> None:
        agent_finding_props: Mock = Mock()

        departament: Mock = Mock()

        departament.id = 1

        agent_finding_props.agent_uuid = ""
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

        agent_auth_props.departament_access = ""
        agent_auth_props.user = ""
        agent_auth_props.password = ""

        agent_auth_service: IService[
            AgentAuthorizationServiceProps, str
        ] = AgentAuthorizationService()

        token: str = agent_auth_service.execute(agent_auth_props)

        self.assertTrue(token)

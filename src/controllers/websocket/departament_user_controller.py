from typing import Dict, TypeAlias, Any, List, Optional

from server import App
from server.websocket import Controller, ConnectionController
from middlewares.websocket import AgentAuthenticationMiddleware
from models import Agent, Departament
from .user_controller import ConnectionUser


JSONType: TypeAlias = Dict[str, Any]


agent_auth_middleware: AgentAuthenticationMiddleware = AgentAuthenticationMiddleware()


class ConnectionDepartamentUser(ConnectionController):
    def __init__(
        self, id_socket: str, uuid: str, departament_uuid: str, name: str, access: str
    ) -> None:
        self.name: str = name
        self.access: str = access
        self.uuid: str = uuid
        self.departament_uuid: str = departament_uuid

        super().__init__(id_socket)

    def __repr__(self) -> str:
        return f"<ConnectionDepartamentUser name={self.name} access={self.access} uuid={self.uuid} departament_uuid={self.departament_uuid} id={self.id}"


@App.websocket.add_controller("/departament_user")
class DepartamentUserController(Controller[ConnectionDepartamentUser]):
    @agent_auth_middleware.apply(None)
    def on_open(
        self,
        connection: ConnectionController,
        auth_user: Agent,
        auth_departament: Departament,
    ) -> Optional[ConnectionDepartamentUser]:
        users_connections_found: List[ConnectionDepartamentUser] = [
            connection
            for connection in self.connections
            if connection.departament_uuid == auth_departament.id_uuid
            and connection.uuid == auth_user.id_uuid
        ]

        if users_connections_found:
            return

        connection_departament_user: ConnectionDepartamentUser = (
            ConnectionDepartamentUser(
                connection.id,
                auth_user.id_uuid,
                auth_departament.id_uuid,
                auth_user.nome,
                auth_user.acesso,
            )
        )

        return connection_departament_user

    def on_send_message_user(self, data: JSONType) -> None:
        pass

    def on_send_message_departament_user(self, data: JSONType) -> None:
        body: str = data["body"]
        departament_user_uuid: str = data["departament_user_uuid"]
        departament_uuid: str = data["departament_uuid"]

        try:
            (departament_user_connection,) = (
                connection
                for connection in self.connections
                if connection.id == App.websocket.global_request.sid
            )

            (departament_user_message_connection,) = (
                connection
                for connection in self.connections
                if connection.departament_uuid == departament_uuid
                and connection.uuid == departament_user_uuid
            )

        except Exception as error:
            print("FALHA AO LOCALIZAR USUÁRIO DE DEPARTAMENTO CONECTADO!", error)

        else:
            message_data: JSONType = {
                "body": body,
                "departament_user_uuid": departament_user_connection.uuid,
                "departament_uuid": departament_user_connection.departament_uuid,
            }

            self.emit(
                "departament_user_message",
                message_data,
                room=departament_user_message_connection.id,
            )

    def on_get_users(self, data: JSONType) -> None:
        socket_id: str = App.websocket.global_request.sid

        user_controller: Controller[ConnectionUser] = App.websocket.get_controller(
            "/user"
        )

        users: List[JSONType] = [
            {
                "nome": "Victor Henrich",
                "email": "victorhenrich993@gmail.com",
                "id": user.id,
            }
            for user in user_controller.connections
        ]

        self.emit("get_users", users, room=socket_id)

    def on_get_departament_users(self) -> None:
        socket_id: str = App.websocket.global_request.sid

        departament_users: List[JSONType] = [
            {
                "name": user.name,
                "username": user.access,
                "departament_user_uuid": user.uuid,
                "departament_uuid": user.departament_uuid,
            }
            for user in self.connections
            if user.id != socket_id
        ]

        self.emit("get_departament_users", departament_users, room=socket_id)

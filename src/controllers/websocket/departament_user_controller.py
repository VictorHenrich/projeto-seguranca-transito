from typing import List, Dict, Any, TypeAlias

from start import app
from server.websocket import Controller
from middlewares.websocket import DepartamentUserAuthenticationMiddleware
from models import UsuarioDepartamento, Departamento
from .user_controller import UserController



JSON: TypeAlias = Dict[str, Any]


@app.websocket.add_controller("/departament_user")
class DepartamentUserController(Controller):
    __departament_users_ids: List[JSON] = []

    @DepartamentUserAuthenticationMiddleware.apply()
    def on_connect(self, auth_user: UsuarioDepartamento, auth_departament: Departamento) -> None:
        socket_id: str = app.websocket.global_request.sid

        DepartamentUserController.__departament_users_ids.append({
            "name": auth_user.nome,
            "uuid": auth_user.id_uuid,
            "departament_uuid": auth_departament.id_uuid,
            "session_id": socket_id
        })

    def on_disconnect(self) -> None:
        socket_id: str = app.websocket.global_request.sid

        for user in DepartamentUserController.__departament_users_ids:
            if user['session_id'] == socket_id:
                DepartamentUserController.__departament_users_ids.remove(user)

    def on_receive_message(self, data: JSON) -> None:
        print('USUÁRIO DEPARTAMENTO RECEBEU A SEGUINTE MENSAGEM:  ', data)

    def on_send_message(self, data: JSON) -> None:
        app.websocket.emit('receive_message', 'OI', namespace="/user")
        print(help(app.websocket.emit))

    def on_get_users(self, data: None) -> None:
        self.emit('get_users', UserController.get)


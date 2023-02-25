from typing import List, Dict, Any

from start import app
from server.websocket import Controller



@app.websocket.add_controller("/departament_user")
class DepartamentUserController(Controller):
    __departament_users_ids: List[str] = []

    def on_connect(self) -> None:
        socket_id: str = app.websocket.global_request.sid

        DepartamentUserController.__departament_users_ids.append(socket_id)

    def on_disconnect(self) -> None:
        socket_id: str = app.websocket.global_request.sid

        DepartamentUserController.__departament_users_ids.remove(socket_id)

    def on_receive_message(self, data: Dict[str, Any]) -> None:
        print('USUÁRIO DEPARTAMENTO RECEBEU A SEGUINTE MENSAGEM:  ', data)

    def on_send_message(self, data: Dict[str, Any]) -> None:
        app.websocket.emit_controller('/user', 'receive_message', data)

from server import SocketServer, CLI
from server.cli import Task


@CLI.add_task("websocket", "run", "r", "Inicializa a aplicação WEBSOCKET")
class RunWebSocket(Task):
    def run(self) -> None:
        import controllers.websocket

        SocketServer.run()

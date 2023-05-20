from server import App
from server.cli import Task


@App.cli.add_task("websocket", "run", "r", "Inicializa a aplicação WEBSOCKET")
class RunWebSocket(Task):
    def run(self) -> None:
        import controllers.websocket

        App.websocket.run()

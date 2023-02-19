from start import app
from server.cli import Task


@app.cli.add_task("websocket", "run", "r", "Inicializa a aplicação WEBSOCKET")
class RunWebSocket(Task):
    def execute(self) -> None:
        import controllers

        app.websocket.run()

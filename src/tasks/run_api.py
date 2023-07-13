from server import HttpServer, CLI
from server.cli import Task


@CLI.add_task("api", "run", "r", "Inicializa a aplicação HTTP")
class RunApi(Task):
    def run(self) -> None:
        import controllers.http

        HttpServer.run()

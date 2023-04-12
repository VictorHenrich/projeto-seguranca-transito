from server import App
from server.cli import Task


@App.cli.add_task("api", "run", "r", "Inicializa a aplicação HTTP")
class RunApi(Task):
    def execute(self, props) -> None:
        import controllers.http.authentication
        import controllers.http.occurrence
        import controllers.http.user

        App.http.run()

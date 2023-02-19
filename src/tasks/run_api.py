from start import app
from server.cli import Task


@app.cli.add_task("api", "run", "r", "Inicializa a aplicação HTTP")
class RunApi(Task):
    def execute(self) -> None:
        import controllers
        import start.routes

        app.http.run()

from server import App
from server.cli import Task


@App.cli.add_task("api", "run", "r", "Inicializa a aplicação HTTP")
class RunApi(Task):
    def execute(self, props) -> None:
        import controllers.http.autenticacao
        import controllers.http.departamento
        import controllers.http.ocorrencias
        import controllers.http.usuarios
        import controllers.http.agentes

        App.http.run()

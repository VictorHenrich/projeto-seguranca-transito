from start import app
from server.cli import Task


@app.cli.add_task("api", "run", "r", "Inicializa a aplicação HTTP")
class RunApi(Task):
    def execute(self) -> None:
        import controllers.http.autenticacao
        import controllers.http.departamento
        import controllers.http.ocorrencias
        import controllers.http.usuarios
        import controllers.http.usuarios_departamento

        app.http.run()

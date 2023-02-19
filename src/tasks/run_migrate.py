from start import app
from server.cli import Task


@app.cli.add_task("database", "migrate", "m", "Inicializa a migração do banco de dados")
class RunMigrate(Task):
    def execute(self) -> None:
        import models

        app.databases.migrate(False)

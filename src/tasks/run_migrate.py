from server import App
from server.cli import Task


@App.cli.add_task("database", "migrate", "m", "Inicializa a migração do banco de dados")
class RunMigrate(Task):
    def execute(self, props) -> None:
        import models

        App.databases.migrate(False)

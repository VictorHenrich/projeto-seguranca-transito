from server import Databases, CLI
from server.cli import Task


@CLI.add_task("database", "migrate", "m", "Inicializa a migração do banco de dados")
class RunMigrate(Task):
    def run(self) -> None:
        import models

        Databases.migrate(True)

from server import App
from server.cli import Task


@App.cli.add_task("amqp", "run", "r", "Inicializa os consumers de AMQP")
class RunConsumers(Task):
    def run(self, props) -> None:
        import consumers

        App.amqp.start_consumers()

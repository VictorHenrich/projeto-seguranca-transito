from server import CLI, AMQPServer
from server.cli import Task


@CLI.add_task("amqp", "run", "r", "Inicializa os consumers de AMQP")
class RunConsumers(Task):
    def run(self) -> None:
        import consumers

        AMQPServer.start_consumers()

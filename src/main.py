from server import AppFactory, CLI
from settings import DATABASE, HTTP, WEBSOCKET, CLI_CONFIG, AMQP


AppFactory.init_server(
    http=HTTP, databases=DATABASE, websocket=WEBSOCKET, cli=CLI_CONFIG, amqp=AMQP
)


if __name__ == "__main__":
    import tasks

    CLI.run()

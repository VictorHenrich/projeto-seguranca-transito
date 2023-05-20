from server import App
from settings import DATABASE, HTTP, WEBSOCKET, CLI, AMQP


App.init_server(http=HTTP, databases=DATABASE, websocket=WEBSOCKET, cli=CLI, amqp=AMQP)


if __name__ == "__main__":
    import tasks

    App.start()

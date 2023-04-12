from .configs import DATABASE, HTTP, WEBSOCKET, CLI, AMQP
from server import App


App.init_server(http=HTTP, databases=DATABASE, websocket=WEBSOCKET, cli=CLI, amqp=None)

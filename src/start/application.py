from .configs import DATABASE, HTTP, WEBSOCKET, CLI
from server import App


App.init_server(http=HTTP, databases=DATABASE, websocket=WEBSOCKET, cli=CLI)

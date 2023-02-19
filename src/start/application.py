from .configs import DATABASE, HTTP, WEBSOCKET, CLI
from server import App, AppFactory


app: App = AppFactory.create(
    http=HTTP, databases=DATABASE, websocket=WEBSOCKET, cli=CLI
)

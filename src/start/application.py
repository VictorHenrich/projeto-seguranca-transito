from .configs import DATABASE, HTTP, WEBSOCKET
from server import App, AppFactory


app: App = AppFactory.create(HTTP, DATABASE, WEBSOCKET)

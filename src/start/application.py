from .configs import DATABASE, HTTP
from server import App, AppFactory


app: App = AppFactory.create(HTTP, DATABASE, None)

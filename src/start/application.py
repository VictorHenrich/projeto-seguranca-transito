from .configs import (
    DATABASE,
    HTTP
)
from services import App, AppFactory



server: App = AppFactory.create(HTTP, DATABASE, None)
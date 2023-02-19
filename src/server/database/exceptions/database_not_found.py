class DatabaseNotFoundError(Exception):
    def __init__(self) -> None:
        super().__init__("Could not find the database")

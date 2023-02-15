class InstanceEngineError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Database does not have the correct instantiation to perform the migration"
        )

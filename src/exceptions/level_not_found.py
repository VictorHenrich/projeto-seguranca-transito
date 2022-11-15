class LevelNotFoundError(Exception):
    def __init__(self) -> None:
        super().__init__('Nível não localizado!')
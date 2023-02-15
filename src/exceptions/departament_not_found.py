class DepartamentNotFoundError(Exception):
    def __init__(self) -> None:
        super().__init__("Acesso de departamento não localizado!")

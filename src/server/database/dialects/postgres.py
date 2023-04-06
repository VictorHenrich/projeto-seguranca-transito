from ..database_builder import DatabaseBuilder


class Postgres(DatabaseBuilder):
    def __init__(self):
        super().__init__(dialect="postgresql", port=5432, driver="psycopg2")

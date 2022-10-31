from .dialect_builder import DialectDefaultBuilder


class Postgres(DialectDefaultBuilder):
    def __init__(self):
        super().__init__(
            name_base="postgresql", 
            port=5432, 
            driver_default="psycopg2", 
            driver_async="asyncpg"
        )
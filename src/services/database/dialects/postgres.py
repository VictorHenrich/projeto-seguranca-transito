from .dialect_builder import DialectDefaultBuilder


class Postgres(DialectDefaultBuilder):
    def __init__(self):
        super().__init__(
            "postgresql", 
            None, 
            5432, 
            None, 
            None, 
            None, 
            "psycopg2", 
            "asyncpg"
        )
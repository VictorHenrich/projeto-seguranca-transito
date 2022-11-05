from .dialect_builder import DialectDefaultBuilder


class MySQL(DialectDefaultBuilder):
    def __init__(self):
        super().__init__(
            dialect="mysql", 
            port=3306, 
            driver_default="pymysql", 
            driver_async="asyncmy"
        )
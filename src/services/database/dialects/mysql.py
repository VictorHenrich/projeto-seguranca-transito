from .dialect_builder import DialectDefaultBuilder


class MySQL(DialectDefaultBuilder):
    def __init__(self):
        super().__init__(
            "mysql", 
            None, 
            3306, 
            None, 
            None, 
            None, 
            "pymysql", 
            "asyncmy"
        )
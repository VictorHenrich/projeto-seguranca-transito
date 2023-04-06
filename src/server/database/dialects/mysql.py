from ..database_builder import DatabaseBuilder


class MySQL(DatabaseBuilder):
    def __init__(self):
        super().__init__(dialect="mysql", port=3306, driver="pymysql")

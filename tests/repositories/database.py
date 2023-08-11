from src.server.database import Database
from src.server.database.dialects import Postgres

database: Database = (
    Postgres()
    .set_dbname("projeto_seguranca_transito")
    .set_host("localhost")
    .set_credentials("postgres", "1234")
    .set_debug(True)
    .build()
)

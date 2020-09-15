from database.postgres import PostgresDB


async def get_conn():
    async with PostgresDB.get_conn() as conn:
        yield conn

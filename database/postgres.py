from typing import Optional

import asyncpg
from asyncpg.pool import Pool


class PostgresDB:
    __pool: Optional[Pool]

    @classmethod
    async def connect(cls):
        cls.__pool = await asyncpg.create_pool('postgresql://lkchat:01480eiD@localhost:5433/lkchat')

    @classmethod
    async def disconnect(cls):
        await cls.__pool.close()

    @classmethod
    def get_conn(cls):
        return cls.__pool.acquire()

from asyncpg import Connection

from orderkeyset import OrderKeySet


class OrderKeySetRepo:

    def __init__(self, conn: Connection):
        self.conn = conn

    async def insert(self,
                     oks: OrderKeySet) -> OrderKeySet:
        sql = '''INSERT INTO orderkeyset
        VALUES ($1, $2, $3, $4)
        RETURNING *; 
        '''
        oks_saved: dict = await self.conn.fetchrow(
            sql,
            oks.order_id,
            oks.dispatcher_key,
            oks.driver_key,
            oks.customer_key
        )
        return OrderKeySet(**oks_saved)

    async def delete(self, order_id: int):
        sql = '''DELETE FROM orderkeyset WHERE order_id = $1'''
        deleted = await self.conn.fetch(sql, order_id)
        return deleted

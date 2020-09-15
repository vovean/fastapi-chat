from typing import Optional, Tuple

from asyncpg import Connection, Record
from fastapi import HTTPException

from message import ChatRole, ChatType
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

    async def get_by_order_id(self, order_id: int) -> OrderKeySet:
        sql = '''SELECT * FROM orderkeyset WHERE order_id=$1'''
        oks: Optional[Record] = await self.conn.fetchrow(sql, order_id)
        if oks is None:
            raise HTTPException(status_code=404, detail=f"Order with id={order_id} not found")
        return OrderKeySet(**oks)

    async def get_token_role(self, token: str) -> Tuple[ChatRole, str]:
        keys = {
            "dispatcher_key": ChatRole.DISPATCHER,
            "customer_key": ChatRole.CUSTOMER,
            "driver_key": ChatRole.DRIVER
        }
        for key, role in keys.items():
            sql = f"SELECT count(*) FROM orderkeyset WHERE {key}=$1"
            res: Record = await self.conn.fetchrow(sql.format(key_type=key), token)
            if res.get("count"):
                return role, key
        raise Exception("Invalid Token")

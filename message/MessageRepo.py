from asyncpg import Connection

from message import DBMessage
from message.messages import RequestMessage


class MessageRepo:
    def __init__(self, conn: Connection):
        self.conn = conn

    async def insert(self, message: RequestMessage) -> DBMessage:
        sql = '''INSERT INTO 
        messages (order_id, sender_role, text)
        VALUES ($1, $2, $3) 
        RETURNING *'''
        message_saved: dict = await self.conn.fetchrow(
            sql,
            message.order_id,
            message.sender_role.value,
            message.text
        )
        return DBMessage(**message_saved)

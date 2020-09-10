from asyncpg import Connection

from message import Message


class MessageRepo:
    def __init__(self, conn: Connection):
        self.conn = conn

    async def insert(self, message: Message) -> Message:
        sql = '''INSERT INTO 
        messages (order_id, sender_token, text)
        VALUES ($1, $2, $2) 
        RETURNING *'''
        message_saved: dict = await self.conn.fetchrow(
            sql,
            message.order_id,
            message.sender_token,
            message.text
        )
        return Message(**message_saved)

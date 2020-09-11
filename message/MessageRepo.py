from typing import List

from asyncpg import Connection

from message import DBMessage
from message.messages import RequestMessage, ChatRole, ChatType


class MessageRepo:
    def __init__(self, conn: Connection):
        self.conn = conn

    async def insert(self, message: RequestMessage) -> DBMessage:
        sql = '''INSERT INTO 
        messages (order_id, sender_role, chat_type, text)
        VALUES ($1, $2, $3, $4) 
        RETURNING *'''
        message_saved: dict = await self.conn.fetchrow(
            sql,
            message.order_id,
            message.sender_role.value,
            message.chat_type.value,
            message.text
        )
        return DBMessage(**message_saved)

    async def get_order_chat_messages(
            self,
            order_id: int,
            chat_with: ChatType,
    ) -> List[DBMessage]:
        sql = '''
        SELECT * FROM messages WHERE 
            order_id=$1 AND 
            chat_type=$2
        ORDER BY sent_at DESC;'''
        rows: List[dict] = await self.conn.fetch(sql, order_id, chat_with.value)
        dbms: List[DBMessage] = [DBMessage(**row) for row in rows]
        return dbms

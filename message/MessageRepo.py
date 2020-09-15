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
            limit: int = 10,
            offset: int = 0
    ) -> List[DBMessage]:
        sql = f'''
        SELECT * FROM messages WHERE 
            order_id=$1 AND 
            chat_type=$2
        ORDER BY sent_at DESC
        LIMIT {limit} OFFSET {offset}'''
        rows: List[dict] = await self.conn.fetch(sql, order_id, chat_with.value)
        dbms: List[DBMessage] = [DBMessage(**row) for row in rows]
        return dbms

    async def get_by_id(self, message_id: int):
        message = await self.conn.fetchrow('SELECT * FROM messages WHERE id=$1', message_id)
        return DBMessage(**message)

    async def get_chat_unread_count(self, reader_role: ChatRole, order_id: int, chat: ChatType):
        sql_last_read_message = '''
        SELECT last_read_message_id FROM read_messages WHERE 
            order_id=$1 AND 
            role=$2 AND 
            chat_type=$3'''
        last_read_message = await self.conn.fetchval(sql_last_read_message, order_id, reader_role.value, chat.value)
        last_read_message = last_read_message or -1
        sql_count_unread = '''
        SELECT count(*) FROM messages WHERE 
        order_id=$1 AND chat_type=$2 AND id>$3'''
        unread_count = await self.conn.fetchval(sql_count_unread, order_id, chat.value, last_read_message)
        return unread_count

    async def read_message(self, reader: ChatRole, message: DBMessage):
        sql = '''
        INSERT INTO read_messages (order_id, chat_type, role, last_read_message_id)  
        VALUES ($1, $2, $3, $4) ON CONFLICT (order_id, chat_type, role) DO UPDATE SET last_read_message_id=$4
        RETURNING last_read_message_id'''
        return await self.conn.fetchval(sql, message.order_id, message.chat_type.value, reader.value, message.id)

    async def get_last_read_message(self, order_id: int, chat: ChatType, role: ChatRole):
        return await self.conn.fetchval('''SELECT last_read_message_id FROM read_messages WHERE 
                                            order_id=$1 AND
                                            chat_type=$2 AND
                                            role=$3''',
                                        order_id, chat.value, role.value)

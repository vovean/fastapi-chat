from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class ChatRole(str, Enum):
    DISPATCHER = 'DSPTCHR'
    DRIVER = 'DRVR'
    CUSTOMER = 'CSTMR'
    SYSTEM = 'SSTM'


class ChatType(str, Enum):
    DRIVER_CHAT = 'DC'
    CUSTOMER_CHAT = 'CC'


class RequestMessage(BaseModel):
    order_id: int
    chat_type: ChatType
    sender_role: ChatRole
    text: str


class DBMessage(BaseModel):
    id: int
    order_id: int
    sender_role: ChatRole  # [ DSPTCHR, DRVR, CSTMR, SSTM ]
    chat_type: ChatType  # [ DC, CC ]
    sent_at: datetime
    text: str


class ChatMessages(BaseModel):
    messages: List[DBMessage]
    last_read_id: Optional[int]
    unread_count: int

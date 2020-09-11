from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class ChatRole(str, Enum):
    DISPATCHER = 'DSPTCHR'
    DRIVER = 'DRVR'
    CUSTOMER = 'CSTMR'


class RequestMessage(BaseModel):
    order_id: int
    sender_role: ChatRole
    receiver_role: ChatRole
    text: str


class DBMessage(BaseModel):
    id: int
    order_id: int
    sender_role: ChatRole
    receiver_role: ChatRole
    sent_at: datetime
    text: str

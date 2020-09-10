from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class SenderRole(Enum):
    DISPATCHER = 'DSPTCHR'
    DRIVER = 'DRVR'
    CUSTOMER = 'CSTMR'


class RequestMessage(BaseModel):
    order_id: int
    sender_role: SenderRole
    text: str


class DBMessage(BaseModel):
    id: int
    order_id: int
    sender_role: SenderRole
    sent_at: datetime
    text: str

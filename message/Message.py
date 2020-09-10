from datetime import datetime

from pydantic import BaseModel


class Message(BaseModel):
    id: int
    order_id: int
    sender_token: str
    sent_at: datetime
    text: str

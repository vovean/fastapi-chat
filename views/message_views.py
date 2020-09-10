from typing import Optional, Union

from fastapi import APIRouter, Header, HTTPException
from starlette.requests import Request

from message import DBMessage, MessageRepo
from message.messages import SenderRole, RequestMessage
from orderkeyset.OrderKeySetRepo import OrderKeySetRepo

router = APIRouter()


@router.post("", response_model=DBMessage)
async def send_message(
        *,
        message: RequestMessage,
        x_token: str = Header(None),
        request: Request
):
    oks_repo = OrderKeySetRepo(request.state.conn)
    oks = await oks_repo.get_by_order_id(message.order_id)
    if (
            message.sender_role == SenderRole.DISPATCHER and x_token != oks.dispatcher_key or
            message.sender_role == SenderRole.DRIVER and x_token != oks.driver_key or
            message.sender_role == SenderRole.CUSTOMER and x_token != oks.customer_key
    ):
        raise HTTPException(status_code=403, detail="Invalid token or sender_role")
    msg_repo = MessageRepo(request.state.conn)
    msg_saved = await msg_repo.insert(message)
    return msg_saved

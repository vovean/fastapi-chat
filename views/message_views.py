from typing import Optional, Union

from fastapi import APIRouter, Header, HTTPException
from starlette.requests import Request

from message import DBMessage, MessageRepo
from message.messages import ChatRole, RequestMessage
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
            message.sender_role == ChatRole.DISPATCHER and x_token != oks.dispatcher_key or
            message.sender_role == ChatRole.DRIVER and x_token != oks.driver_key or
            message.sender_role == ChatRole.CUSTOMER and x_token != oks.customer_key
    ):
        raise HTTPException(status_code=403, detail="Invalid X-Token or sender_role")
    msg_repo = MessageRepo(request.state.conn)
    msg_saved = await msg_repo.insert(message)
    return msg_saved

@router.get("/{order_id}/{chat_with}")
async def get_order_chat_history(
        *,
        order_id: int,
        chat_with: ChatRole,
        x_token: str = Header(None),
        request: Request
):
    oks_repo = OrderKeySetRepo(request.state.conn)
    oks = await oks_repo.get_by_order_id(order_id)
    if x_token != oks.dispatcher_key:
        if chat_with == ChatRole.DRIVER and x_token != oks.driver_key:
            raise HTTPException(status_code=403, detail="Invalid X-Token or order_id or receiver_role")
        if chat_with == ChatRole.CUSTOMER and x_token != oks.customer_key:
            raise HTTPException(status_code=403, detail="Invalid X-Token or order_id or receiver_role")
    message_repo = MessageRepo(request.state.conn)
    return await message_repo.get_order_chat_messages(order_id, chat_with)

from typing import Optional, Union

from fastapi import APIRouter, Header, HTTPException, Body, Path
from starlette.requests import Request

from message import DBMessage, MessageRepo
from message.messages import ChatRole, RequestMessage, ChatType
from orderkeyset import OrderKeySet
from orderkeyset.OrderKeySetRepo import OrderKeySetRepo

router = APIRouter()


def get_sender(oks: OrderKeySet, token: str):
    token2role = {
        oks.dispatcher_key: ChatRole.DISPATCHER,
        oks.driver_key: ChatRole.DRIVER,
        oks.customer_key: ChatRole.CUSTOMER,
    }
    if token not in token2role:
        raise HTTPException(status_code=403, detail="Invalid X-Token")
    return token2role[token]


@router.post("/{order_id}/{chat_type}", response_model=DBMessage)
async def send_message(
        *,
        order_id: int = Path(...),
        chat_type: ChatType = Path(...),
        text: str = Body(..., embed=True),
        x_token: str = Header(None),
        request: Request
):
    oks_repo = OrderKeySetRepo(request.state.conn)
    oks = await oks_repo.get_by_order_id(order_id)
    sender_role = get_sender(oks, x_token)
    msg_repo = MessageRepo(request.state.conn)
    message = RequestMessage(
        order_id=order_id,
        sender_role=sender_role,
        chat_type=chat_type,
        text=text
    )
    msg_saved = await msg_repo.insert(message)
    return msg_saved


@router.get("/{order_id}/{chat_type}")
async def get_order_chat_history(
        *,
        order_id: int,
        chat_type: ChatType,
        x_token: str = Header(None),
        request: Request
):
    oks_repo = OrderKeySetRepo(request.state.conn)
    oks = await oks_repo.get_by_order_id(order_id)
    if x_token != oks.dispatcher_key:
        if chat_type == ChatType.DRIVER_CHAT and x_token != oks.driver_key:
            raise HTTPException(status_code=403, detail="Invalid X-Token or order_id or chat_type")
        if chat_type == ChatType.CUSTOMER_CHAT and x_token != oks.customer_key:
            raise HTTPException(status_code=403, detail="Invalid X-Token or order_id or chat_type")
    message_repo = MessageRepo(request.state.conn)
    return await message_repo.get_order_chat_messages(order_id, chat_type)

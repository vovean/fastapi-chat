from asyncpg import Connection
from fastapi import APIRouter, Header, HTTPException, Body, Path, Depends, Query
from starlette.requests import Request

from message import DBMessage, MessageRepo
from message.messages import RequestMessage, ChatType
from orderkeyset.OrderKeySetRepo import OrderKeySetRepo
from views.dependencies import get_conn
from views.utils import get_sender
from ws_notifier.notifier import notifier

router = APIRouter()


@router.post("/{order_id}/{chat_type}", response_model=DBMessage)
async def send_message(
        *,
        order_id: int = Path(...),
        chat_type: ChatType = Path(...),
        text: str = Body(..., embed=True),
        x_token: str = Header(None),
        conn: Connection = Depends(get_conn)
):
    oks_repo = OrderKeySetRepo(conn)
    oks = await oks_repo.get_by_order_id(order_id)
    sender_role = get_sender(oks, x_token)
    msg_repo = MessageRepo(conn)
    message = RequestMessage(
        order_id=order_id,
        sender_role=sender_role,
        chat_type=chat_type,
        text=text
    )
    msg_saved = await msg_repo.insert(message)
    await notifier.notify(msg_saved)
    return msg_saved


@router.get("/{order_id}/{chat_type}")
async def get_order_chat_history(
        *,
        order_id: int = Path(...),
        chat_type: ChatType = Path(...),
        limit: int = Query(10, gt=0),
        offset: int = Query(0, ge=0),
        x_token: str = Header(None),
        conn: Connection = Depends(get_conn)
):
    oks_repo = OrderKeySetRepo(conn)
    oks = await oks_repo.get_by_order_id(order_id)
    if x_token != oks.dispatcher_key:
        if chat_type == ChatType.DRIVER_CHAT and x_token != oks.driver_key:
            raise HTTPException(status_code=403, detail="Invalid X-Token or order_id or chat_type")
        if chat_type == ChatType.CUSTOMER_CHAT and x_token != oks.customer_key:
            raise HTTPException(status_code=403, detail="Invalid X-Token or order_id or chat_type")
    message_repo = MessageRepo(conn)
    return await message_repo.get_order_chat_messages(order_id, chat_type, limit, offset)

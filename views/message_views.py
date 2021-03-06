import hashlib
import os

import aiofiles
from asyncpg import Connection
from fastapi import APIRouter, Header, HTTPException, Body, Path, Depends, Query, UploadFile, File

from message import DBMessage, MessageRepo
from message.messages import RequestMessage, ChatType, ChatMessages, ChatRole
from orderkeyset.OrderKeySetRepo import OrderKeySetRepo
from views.dependencies import get_conn
from views.utils import get_sender, check_role_chat
from ws_notifier.notifier import notifier

router = APIRouter()


@router.post("/{order_id}/{chat_type}", response_model=DBMessage)
async def send_message(
        *,
        order_id: int = Path(...),
        chat_type: ChatType = Path(...),
        text: str = Body(..., embed=True),
        file=File(None),
        x_token: str = Header(None),
        conn: Connection = Depends(get_conn)
):
    oks_repo = OrderKeySetRepo(conn)
    oks = await oks_repo.get_by_order_id(order_id)
    sender_role = get_sender(oks, x_token)
    check_role_chat(sender_role, chat_type)
    msg_repo = MessageRepo(conn)
    message = RequestMessage(
        order_id=order_id,
        sender_role=sender_role,
        chat_type=chat_type,
        text=text
    )
    updated_msg = await msg_repo.insert(message)
    # save file
    if file is not None:
        data = await file.read()
        name = f"{hashlib.md5(f'{updated_msg.id}.{file.filename}'.encode()).hexdigest()}{os.path.splitext(file.filename)[-1]}"
        path = fr"files/{name}"
        async with aiofiles.open(path, "wb") as f:
            await f.write(data)
        # update db record
        updated_msg = await msg_repo.set_file(updated_msg.id, path)
    await notifier.notify(updated_msg)
    await msg_repo.read_message(sender_role, updated_msg)
    return updated_msg


@router.get("/{order_id}/{chat_type}", response_model=ChatMessages)
async def get_order_chat_history(
        *,
        order_id: int = Path(...),
        chat_type: ChatType = Path(...),
        limit: int = Query(3000, gt=0),
        offset: int = Query(0, ge=0),
        x_token: str = Header(None),
        conn: Connection = Depends(get_conn)
):
    oks_repo = OrderKeySetRepo(conn)
    oks = await oks_repo.get_by_order_id(order_id)
    role = get_sender(oks, x_token)
    check_role_chat(role, chat_type)
    message_repo = MessageRepo(conn)
    messages = await message_repo.get_order_chat_messages(order_id, chat_type, limit, offset)
    last_read_id = await message_repo.get_last_read_message_id(order_id, chat_type, role)
    unread_count = await message_repo.get_chat_unread_count(role, order_id, chat_type)
    return ChatMessages(messages=messages, last_read_id=last_read_id, unread_count=unread_count)


@router.get("/{order_id}/{chat_type}/new")
async def get_chat_unread_count(
        order_id: int = Path(...),
        chat_type: ChatType = Path(...),
        x_token: str = Header(None),
        conn: Connection = Depends(get_conn)
):
    oks_repo = OrderKeySetRepo(conn)
    oks = await oks_repo.get_by_order_id(order_id)
    sender_role = get_sender(oks, x_token)
    check_role_chat(sender_role, chat_type)
    message_repo = MessageRepo(conn)
    return await message_repo.get_chat_unread_count(sender_role, order_id, chat_type)


@router.post("/{order_id}/{chat_type}/read")
async def read_message(
        order_id: int = Path(...),
        chat_type: ChatType = Path(...),
        message_id: int = Body(..., embed=True),
        x_token: str = Header(None),
        conn: Connection = Depends(get_conn)
):
    oks_repo = OrderKeySetRepo(conn)
    oks = await oks_repo.get_by_order_id(order_id)
    sender_role = get_sender(oks, x_token)
    message_repo = MessageRepo(conn)
    message = await message_repo.get_by_id(message_id)
    if chat_type != message.chat_type:
        return HTTPException(status_code=400, detail="This message if from another chat")
    return await message_repo.read_message(sender_role, message)

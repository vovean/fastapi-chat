from asyncpg import Connection
from fastapi import APIRouter, Path, Header, HTTPException, Depends, Query
from starlette.websockets import WebSocket, WebSocketDisconnect

from orderkeyset.OrderKeySetRepo import OrderKeySetRepo
from views.dependencies import get_conn
from views.utils import get_sender
from ws_notifier.notifier import notifier

router = APIRouter()


@router.websocket("/{order_id}")
async def subscribe(
        *,
        order_id: int = Path(...),
        x_token: str = Query(...),
        ws: WebSocket,
        conn: Connection = Depends(get_conn)
):
    oks = await OrderKeySetRepo(conn).get_by_order_id(order_id)
    try:
        sender_role = get_sender(oks, x_token)
        await notifier.subscribe(order_id, sender_role, ws)
    # в ws мы не можем послать HTTPException поэтому шлем текст и закрываем ws
    except HTTPException as e:
        await ws.accept()
        await ws.send_text(e.detail)
        await ws.close()
        return
    # вероятно, чтобы ws не закрылся нам нужно держать этот метод запущенным
    try:
        while True:
            await ws.receive_text()
            await ws.send_text("This channel is for notifications only. No incoming data is accepted")
    except WebSocketDisconnect:
        notifier.remove(order_id, sender_role)

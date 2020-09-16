from asyncpg import Connection
from fastapi import Body, APIRouter, Depends, Header, HTTPException

from orderkeyset import OrderKeySet
from orderkeyset.OrderKeySetRepo import OrderKeySetRepo
from settings import get_settings
from views.dependencies import get_conn
from views.utils import get_sender

router = APIRouter()


@router.post("/order")
async def create_order(
        *,
        oks: OrderKeySet = Body(...),
        x_token: str = Header(None),
        conn: Connection = Depends(get_conn)
):
    if x_token != get_settings().system_token:
        raise HTTPException(status_code=403, detail="Only system")
    oks_repo = OrderKeySetRepo(conn)
    inserted = await oks_repo.insert(oks)
    return inserted


@router.delete('/order/{order_id}')
async def delete_order(order_id: int, x_token: str = Header(None), conn: Connection = Depends(get_conn)):
    if x_token != get_settings().system_token:
        raise HTTPException(status_code=403, detail="Only system")
    oks_repo = OrderKeySetRepo(conn)
    deleted = await oks_repo.delete(order_id)
    return deleted

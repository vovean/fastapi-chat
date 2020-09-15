from asyncpg import Connection
from fastapi import Body, APIRouter, Depends

from orderkeyset import OrderKeySet
from orderkeyset.OrderKeySetRepo import OrderKeySetRepo
from views.dependencies import get_conn

router = APIRouter()


@router.post("/order")
async def create_order(
        *,
        oks: OrderKeySet = Body(...),
        conn: Connection = Depends(get_conn)
):
    oks_repo = OrderKeySetRepo(conn)
    inserted = await oks_repo.insert(oks)
    return inserted


@router.delete('/order/{order_id}')
async def delete_order(order_id: int, conn: Connection = Depends(get_conn)):
    oks_repo = OrderKeySetRepo(conn)
    deleted = await oks_repo.delete(order_id)
    return deleted

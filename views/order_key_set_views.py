from asyncpg import Connection
from fastapi import Body, APIRouter
from starlette.requests import Request

from database.postgres import PostgresDB
from orderkeyset import OrderKeySet
from orderkeyset.OrderKeySetRepo import OrderKeySetRepo

router = APIRouter()


@router.post("/order")
async def create_order(
        *,
        oks: OrderKeySet = Body(...),
        request: Request
):
    oks_repo = OrderKeySetRepo(request.state.conn)
    inserted = await oks_repo.insert(oks)
    return inserted


@router.delete('/order/{order_id}')
async def delete_order(order_id: int, request: Request):
    oks_repo = OrderKeySetRepo(request.state.conn)
    deleted = await oks_repo.delete(order_id)
    return deleted

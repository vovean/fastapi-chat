from typing import List, Optional

import asyncpg
from asyncpg import Connection, Record
from asyncpg.pool import Pool
from fastapi import FastAPI, Query, Body
from typing import Union

from orderkeyset import OrderKeySet
from orderkeyset.OrderKeySetRepo import OrderKeySetRepo

app = FastAPI()
pool: Optional[Pool] = None


@app.on_event("startup")
async def on_startup():
    global pool
    pool = await asyncpg.create_pool('postgresql://lkchat:01480eiD@localhost:5433/lkchat')


@app.on_event("shutdown")
async def on_shutdown():
    global pool
    await pool.close()


@app.post("/order")
async def create_order(
        oks: OrderKeySet = Body(...)
):
    conn: Connection
    async with pool.acquire() as conn:
        oks_repo = OrderKeySetRepo(conn)
        inserted = await oks_repo.insert(**oks.dict())
        return inserted


@app.delete('/order/{order_id}')
async def delete_order(order_id: int):
    conn: Connection
    async with pool.acquire() as conn:
        oks_repo = OrderKeySetRepo(conn)
        deleted = await oks_repo.delete(order_id)
        return deleted

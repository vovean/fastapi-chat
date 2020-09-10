import asyncpg
from fastapi import FastAPI

from database.postgres import PostgresDB
from middleware.connection_middleware import ConnectionMiddleware
from views.order_key_set_views import router as oks_router
from views.message_views import router as message_router

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await PostgresDB.connect()


@app.on_event("shutdown")
async def on_shutdown():
    await PostgresDB.disconnect()


app.add_middleware(ConnectionMiddleware)

routers = {
    "/oks": oks_router,
    "/messages": message_router
}

for prefix, router in routers.items():
    app.include_router(router, prefix=prefix)

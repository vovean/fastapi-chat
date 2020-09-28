from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.postgres import PostgresDB
from views.message_views import router as message_router
from views.order_key_set_views import router as oks_router
from views.ws_views import router as ws_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=("GET", "POST", "OPTIONS"),
    allow_headers=("*",),
    allow_credentials=True
)


@app.on_event("startup")
async def on_startup():
    await PostgresDB.connect()


@app.on_event("shutdown")
async def on_shutdown():
    await PostgresDB.disconnect()


routers = {
    "/oks": oks_router,
    "/order_chat": message_router,
    "/ws": ws_router,
}

for prefix, router in routers.items():
    app.include_router(router, prefix=prefix)

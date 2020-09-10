from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from database.postgres import PostgresDB


class ConnectionMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        print("conn middleware called")
        async with PostgresDB.get_conn() as conn:
            request.state.conn = conn
            response = await call_next(request)
        print("close conn")
        return response

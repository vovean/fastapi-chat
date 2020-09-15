from fastapi import HTTPException

from message import ChatRole
from orderkeyset import OrderKeySet


def get_sender(oks: OrderKeySet, token: str):
    token2role = {
        oks.dispatcher_key: ChatRole.DISPATCHER,
        oks.driver_key: ChatRole.DRIVER,
        oks.customer_key: ChatRole.CUSTOMER,
    }
    if token not in token2role:
        raise HTTPException(status_code=403, detail="Invalid X-Token")
    return token2role[token]

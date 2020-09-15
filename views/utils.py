from fastapi import HTTPException

from message import ChatRole, ChatType
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


def check_role_chat(role: ChatRole, chat: ChatType):
    if (
            role == ChatRole.DRIVER and chat != ChatType.DRIVER_CHAT or
            role == ChatRole.CUSTOMER and chat != ChatType.CUSTOMER_CHAT
    ):
        raise HTTPException(status_code=403, detail="You have no access to this chat")

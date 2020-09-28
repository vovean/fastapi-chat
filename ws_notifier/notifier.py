from typing import Dict, Optional, List

from starlette.websockets import WebSocket

from message import ChatRole, ChatType, DBMessage


class Notifier:
    connections: Dict[int, Dict[ChatRole, Optional[WebSocket]]] = {}

    async def subscribe(self, order_id: int, role: ChatRole, ws: WebSocket):
        await ws.accept()
        if not self.connections.get(order_id):
            self.connections[order_id] = dict()
        self.connections[order_id][role] = ws

    def remove(self, order_id: int, role: ChatRole):
        self.connections[order_id][role] = None

    async def notify(self, message: DBMessage):
        # check existing order
        if not self.connections.get(message.order_id):
            self.connections[message.order_id] = dict()
        # add dispatcher to receivers
        connections: Dict[ChatRole, WebSocket] = {
            ChatRole.DISPATCHER: self.connections[message.order_id].get(ChatRole.DISPATCHER)
        }
        # add driver or customer to receivers
        if message.chat_type == ChatType.CUSTOMER_CHAT:
            connections[ChatRole.CUSTOMER] = self.connections[message.order_id].get(ChatRole.CUSTOMER)
        elif message.chat_type == ChatType.DRIVER_CHAT:
            connections[ChatRole.DRIVER] = self.connections[message.order_id].get(ChatRole.DRIVER)
        # notify every receiver
        for role, conn in connections.items():
            # Если ws закрылся, то выкинется ошибка и тогда мы удаляем этот ws
            try:
                if conn:
                    await conn.send_json(message.json())
                    self.connections[message.order_id][role] = conn
            except:
                self.remove(message.order_id, role)


notifier = Notifier()

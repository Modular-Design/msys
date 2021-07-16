from typing import Optional, List
import uuid
from ..interfaces import INode
from ..core import Module
from fastapi import WebSocket

class Instance:
    def __init__(self, id: Optional[str] = None,
                 module: Optional[Module] = None,
                 name: Optional[str] = "",
                 description: Optional[str] = "",
                 ):
        if id is None:
            id = str(uuid.uuid4())
        self.id = id

        if not module:
            module = Module()

        self.module = module

        if name:
            self.module.meta.name = name

        if description:
            self.module.meta.description = description

        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    def nof_connections(self):
        return len(self.active_connections)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def publish(self, topic: str, address: list, content: dict):
        # await endpoint.publish([status.value], content)
        msg = dict(topic=topic, receiver=address, content=content)
        # print(msg)
        print("[API]: " + json.dumps(msg))
        await self.broadcast(json.dumps(msg))
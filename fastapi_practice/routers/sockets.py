import json

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlmodel import Session, select

from fastapi_practice.cores.database import get_db
from fastapi_practice.cores.hashing import Hash
from fastapi_practice.cores.models import Chat, User

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}  

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        self.active_connections.pop(user_id, None)

    async def send_personal_message(self, message: str, user_id: int):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/{username}/{password}/{receiver_name}")
async def websocket_endpoint(
    websocket: WebSocket,
    username: str,
    password: str,
    receiver_name: str,
    db: Session = Depends(get_db),
):
    user = db.exec(select(User).where(User.name == username)).first()
    if not user or not Hash.verify(user.password, password):
        await websocket.close(code=1008)
        return

 
    receiver = db.exec(select(User).where(User.name == receiver_name)).first()
    if not receiver:
        await websocket.close(code=1008)
        return

    await manager.connect(websocket, user.id)


    chats = db.exec(
        select(Chat)
        .where(
            ((Chat.user_id == user.id) & (Chat.receiver_id == receiver.id))
            | ((Chat.user_id == receiver.id) & (Chat.receiver_id == user.id))
        )
        .order_by(Chat.timestamp)
    ).all()

    for chat in chats:
        sender_name = db.get(User, chat.user_id).name
        receiver_name_db = db.get(User, chat.receiver_id).name
        await websocket.send_text(
            f"[{chat.timestamp}] {sender_name} -> {receiver_name_db}: {chat.message}"
        )

    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            message = payload.get("message")

            new_chat = Chat(
                user_id=user.id, receiver_id=receiver.id, message=message
            )
            db.add(new_chat)
            db.commit()
            db.refresh(new_chat)
            await manager.send_personal_message(
                f"You -> {receiver.name}: {message}", user.id
            )
            await manager.send_personal_message(
                f"{user.name} -> You: {message}", receiver.id
            )

    except WebSocketDisconnect:
        manager.disconnect(user.id)
        print(f"{user.name} disconnected")

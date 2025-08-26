from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlmodel import Session, select

from fastapi_practice.cores.database import get_db  # your db session
from fastapi_practice.cores.hashing import Hash
from fastapi_practice.cores.models import Chat, User

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}  # user_id -> ws

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        self.active_connections.pop(user_id, None)

    async def broadcast(self, message: str):
        for ws in self.active_connections.values():
            await ws.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/{username}/{password}")
async def websocket_endpoint(
    websocket: WebSocket,
    username: str,
    password: str,
    db: Session = Depends(get_db),
):
    # 1. Authenticate
    statement = select(User).where(User.name == username)
    result = db.exec(statement).first()
    if not result or not Hash.verify(result.password, password):
        await websocket.close(code=1008)  # policy violation
        return

    user = result

    # 2. Connect user
    await manager.connect(websocket, user.id)

    # 3. Send old messages
    chats = db.exec(select(Chat).order_by(Chat.timestamp)).all()
    for chat in chats:
        await websocket.send_text(
            f"[{chat.timestamp}] User#{chat.sender_id}: {chat.message}"
        )

    try:
        while True:
            data = await websocket.receive_text()
            # 4. Save new message
            new_chat = Chat(user_id=user.id, message=data)
            db.add(new_chat)
            db.commit()
            db.refresh(new_chat)

            # 5. Broadcast to everyone
            await manager.broadcast(f"{user.name}: {data}")

    except WebSocketDisconnect:
        manager.disconnect(user.id)
        await manager.broadcast(f"{user.name} left the chat")

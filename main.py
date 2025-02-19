from fastapi import FastAPI, WebSocket, WebSocketDisconnect 
from sqlalchemy import create_engine, Column, Integer, String, DateTime, text
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 
from datetime import datetime 
import json 

app = FastAPI()

# Database setup 
DATABASE_URL = "postgresql://postgres@localhost/chat_app"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

with engine.connect() as conn:
    result = conn.execute(text("SELECT current_user;"))
    print("Connected as:", result.scalar())

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class OnlineUser(Base):
    __tablename__ = "online_users"
    username = Column(String, primary_key=True)
    last_seen = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine, checkfirst=True)
#inspector = inspect(engine)
#print(inspector.get_table_names())

# WebSocket manager 
class ConnectionManager:
    def __init__(self):
        self.active_connections = {} 

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[username] = websocket 

    def disconnect(self, username: str):
        if username in self.active_connections: 
            del self.active_connections[username]

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)
    db = SessionLocal()
    db.add(OnlineUser(username=username))
    db.commit()
    try:
        while True:
            data = await websocket.receive_text()
            message_data = {"username": username, "message": data}
            await manager.broadcast(json.dumps(message_data))

            # save message to database 
            db_message = Message(username=username, message=data)
            db.add(db_message)
            db.commit()
    except WebSocketDisconnect:
        manager.disconnect(username)
        await manager.broadcast(json.dumps({"username": username, "message": "left the chat"}))
        db.query(OnlineUser).filter(OnlineUser.username == username).delete()
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app, host="0.0.0.0", port=8000)

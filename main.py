from fastapi import FastAPI, WebSocket, WebSocketDisconnect 
from sqlalchemy import create_engine, Column, Integer, String, DateTime, text
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 
from datetime import datetime 
import json 
import asyncio

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Chat App!"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message receved: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")

@app.get("/api/messages")
def get_messages():
    return {"messages": ["Hello", "World"]}

# Database setup 
DATABASE_URL = "postgresql://postgres:123@localhost:5432/chat_app"
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, pool_timeout=30)
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
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error sending message: {e}")

manager = ConnectionManager()

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)
    
    db = SessionLocal()
    try:
        db.add(OnlineUser(username=username))
        db.commit()

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
        #await websocket.close()

if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app, host="0.0.0.0", port=8000)

import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

api = FastAPI()

MONGO_DB="mongodb+srv://coderstrings:Admitnow%4012345@cluster0.zhngv.mongodb.net/coders?retryWrites=true&w=majority"

client = AsyncIOMotorClient(str(MONGO_DB),tls=True, tlsAllowInvalidCertificates=True)
db = client.docdb
doc_collection = db.doc_collection


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "127.0.0.1:3000",
    "localhost:3000",
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@api.get("/")
async def root():
    return {"message": "Hello World"}

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=origins)

# wrap with ASGI application
app = socketio.ASGIApp(sio, api)


@sio.on('*')
def catch_all(event, sid, data):
    pass

@sio.on("get-document")
def get_document(sid):
    pass

@sio.on("save-document")
def save_document(sid):
    pass

@sio.on("send-changes")
def send_changes(sid):
    pass

@sio.event
async def connect(sid, environ, auth):
    await db.doc_collection.find_one({'i': {'$lt': 1}})
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)




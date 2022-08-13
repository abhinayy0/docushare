import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from random_object_id import generate
import logging
import json
import os

with open("settings.json", "r") as f:
    config = json.loads(f.read())

logger = logging.getLogger(__name__)

api = FastAPI()
api.doc2uid = {}
if config["MONGO_DB_URL"] == "":
    MONGO_DB = os.environ["MONGO_DB"]
else:
    MONGO_DB = config["MONGO_DB_URL"]
try:
    client = AsyncIOMotorClient(str(MONGO_DB),tls=True, tlsAllowInvalidCertificates=True)
except: 
    print("Unable to start application database connection not available")

db = client.docdb
doc_collection = db.doc_collection


origins = [
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
    return ["Docushare api"]

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=origins)
app = socketio.ASGIApp(sio, api)


async def find_or_create_doc(id):
    if not id:
        return
    
    document = await db.doc_collection.find_one( {"_id": ObjectId(id)})
    if document:
        return document
    return await db.doc_collection.insert_one({"_id": ObjectId(id), "data":""})


@sio.on("get-document")
async def get_document(sid, doc_id):
    api.doc2uid[doc_id] = api.doc2uid.get(doc_id, generate())
    doc_id = api.doc2uid[doc_id] 
    data = await find_or_create_doc(doc_id)
    sio.enter_room(sid, room=doc_id)
    data = await find_or_create_doc(doc_id)
    await sio.emit("load-document", data["data"])

@sio.on("save-document")
async def save_document(sid, doc_id, data):    
    api.doc2uid[doc_id] = api.doc2uid.get(doc_id, generate())
    hex_doc_id = api.doc2uid[doc_id] 
    await db.doc_collection.update_one({ "_id":ObjectId(hex_doc_id) }, {'$set': {'data': data}})
    
@sio.on("send-changes")
async def send_changes(sid, delta):
    await sio.emit('receive-changes', delta, broadcast=True, include_self=False)

@sio.event
async def connect(sid, environ, auth):
    logger.debug("Connected from socket")

@sio.event
def disconnect(sid):
    logger.debug("Disconnected from socket")




from pydantic import BaseModel
from bson.objectid import ObjectId

class DocSchema(BaseModel):
    data : str
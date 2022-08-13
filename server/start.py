import json
import uvicorn
import os

with open("settings.json", "r") as f:
    config = json.loads(f.read())
try:
    os.system("source .env")
except:
    pass
if config["DEBUG"]:
    os.system("uvicorn app:app --reload")
else:
    os.system("uvicorn app:app")
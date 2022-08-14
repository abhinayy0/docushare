import json
import uvicorn
import os

with open("settings.json", "r") as f:
    config = json.loads(f.read())
try:
    os.system("set -o allexport")
    os.system("source .env")
    os.system("set +o allexport") 
except:
    print("exception")
    pass
if config["DEBUG"]:
    os.system("uvicorn app:app --reload")
elif config["server"] == "uvicorn":
    os.system("uvicorn app:app")
else:
    os.system("gunicorn -w 1 -k uvicorn.workers.UvicornWorker app:app")
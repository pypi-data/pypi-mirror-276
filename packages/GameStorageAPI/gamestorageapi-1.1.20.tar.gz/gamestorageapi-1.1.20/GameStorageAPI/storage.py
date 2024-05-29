import json
import threading
from GameStorageAPI.game import CheckGame

StorageFile = "storage.json"

def SaveStorage(data: dict):
    with open(StorageFile, "w") as f:
        f.write(json.dumps(data, indent=4))

def LoadStorage() -> dict:
    thread = threading.Thread(target=CheckGame)
    thread.start()
    data = {}
    try:
        with open(StorageFile, "r") as f:
            data = json.loads(f.read())
            f.close()
    except Exception:
        with open(StorageFile, "w") as f:
            f.write(json.dumps(data, indent=4))
    return data
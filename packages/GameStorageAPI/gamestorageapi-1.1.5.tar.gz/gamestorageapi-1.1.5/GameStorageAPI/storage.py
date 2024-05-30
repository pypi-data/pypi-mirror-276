import json
import threading
from GameStorageAPI.game import CheckGame

DATA_FILE = "storage.json"

def SaveStorage(data: dict):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def LoadStorage() -> dict:
    thread = threading.Thread(target=CheckGame)
    thread.start()
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
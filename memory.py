import json
import os

def load_session(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_session(path, session):
    with open(path, "w") as f:
        json.dump(session, f, indent=2)

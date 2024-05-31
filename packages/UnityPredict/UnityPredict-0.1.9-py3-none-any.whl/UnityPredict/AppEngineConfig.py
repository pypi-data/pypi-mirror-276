from enum import Enum
from pydantic import BaseModel
import json
import os

class AppEngineConfig (BaseModel):
    TEMP_EXEC_DIR: str = os.getcwd()
    UPT_API_KEY: str = ""
    MODEL_DIR: str = os.path.join(os.getcwd(), "models")
    REQUEST_DIR: str = os.path.join(os.getcwd(), "requests")
    SAVE_CONTEXT: bool = True

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
import json
import uuid
import re
from typing import Any, List

class Validate:

    def is_json(self, jsonData:str) -> bool:
        try:
            json.loads(jsonData)
            
            return True
        except ValueError:
            return False
    
    def is_uuid(self, value:str) -> bool:
        try:
            self.is_empty(value)
            uuid.UUID(value)
    
            return True
        except ValueError:
            return False

    def is_empty(self, value:any) -> bool:
        try:
            if not value or len(value) == 0:
                return False

            return True
        except ValueError:
            return False
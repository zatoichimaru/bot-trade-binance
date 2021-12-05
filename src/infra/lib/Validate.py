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
            if(self.is_empty(value) == False):
                uuid.UUID(value)
                return True

            return False 
        except ValueError:
            return False

    def is_empty(self, value:str) -> bool:
        try:
            return (len(value) <= 0) == True
        except ValueError as error:
            raise Exception("{} - Fail valueError [{}]".format(__class__, error))
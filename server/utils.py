from enum import Enum
import json
import time


class ResponseStatus(Enum):
    OK = "ok"
    ERROR = "err"


DEFAULT_ERROR_MESSAGE = "Request failed"
class ResponseMessage:
    def __init__(self, status=ResponseStatus.OK, data=None, err_message: str = None):
        self.status = status.value
        self.timestamp = round(time.time() * 1000)
        
        if status == ResponseStatus.ERROR:
            self.message = err_message if err_message else DEFAULT_ERROR_MESSAGE
            return
        
        self.data = data

    def jsonify(self):
        return json.dumps(self.__dict__)

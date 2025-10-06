from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi import FastAPI



class MCP(FastAPI):
    def __init__(self):
        super().__init__()
        self.init_time: str = datetime.now(tz=ZoneInfo("Europe/Istanbul"))
    

    def resource(self, path: str, **kwargs):
        return self.get(path=path, **kwargs)
    
    
    def tool(self, path: str, **kwargs):
        return self.post(path=path, **kwargs)


    def uptime(self):
        return datetime.now(tz=ZoneInfo("Europe/Istanbul")) - self.init_time



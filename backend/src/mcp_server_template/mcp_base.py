from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi import FastAPI



class MCP(FastAPI):
    def __init__(self):
        super().__init__()
        self.init_time: str = datetime.now(tz=ZoneInfo("Europe/Istanbul"))


    def ping_server(self):
        pass


    def uptime(self):
        return datetime.now(tz=ZoneInfo("Europe/Istanbul")) - self.init_time



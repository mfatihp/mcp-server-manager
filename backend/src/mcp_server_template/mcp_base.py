from datetime import datetime
from zoneinfo import ZoneInfo


class MCP:
    def __init__(self):
        self.init_time: str = datetime.now(tz=ZoneInfo("Europe/Istanbul"))

    def ping_server(self):
        pass

    def uptime(self):
        return datetime.now(tz=ZoneInfo("Europe/Istanbul")) - self.init_time
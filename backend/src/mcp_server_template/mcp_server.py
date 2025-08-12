from datetime import datetime
from zoneinfo import ZoneInfo


class MCP:
    def __init__(self):
        self.init_time: str = datetime.now(tz=ZoneInfo("Europe/Istanbul"))
        self.uptime:str

    def ping_server(self):
        pass

    def calculate_uptime(self):
        pass



class Tool(MCP):
    def __init__(self):
        super().__init__()


    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print("Hello mars")

            return func(*args, **kwargs)
        return wrapper




class Resource(MCP):
    def __init__(self):
        super().__init__()
    

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print("Hello mars")

            return func(*args, **kwargs)
        return wrapper
    

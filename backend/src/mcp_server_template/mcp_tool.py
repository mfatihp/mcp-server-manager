from mcp_base import MCP


class Tool(MCP):
    def __init__(self):
        super().__init__()


    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print("Hello mars")

            return func(*args, **kwargs)
        return wrapper
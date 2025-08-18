from mcp_base import MCP


class Tool(MCP):
    def __init__(self):
        super().__init__()


tool = Tool()







if __name__ == "__main__":
    import uvicorn

    @tool.get("/")
    def add():
        return 1 + 2

    uvicorn.run(tool)
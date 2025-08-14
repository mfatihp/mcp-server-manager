from mcp_base import MCP


class Tool(MCP):
    def __init__(self):
        super().__init__()


tool = Tool()





@tool.get("/")
def add():
    return 1 + 2



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(tool)
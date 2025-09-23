
from mcp_utils.mcp_tool import Tool



tool = Tool()

@tool.get("/Test1")
def Test1():
    return 'Hello'


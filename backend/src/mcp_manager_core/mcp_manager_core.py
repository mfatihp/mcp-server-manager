from fastapi import FastAPI



core = FastAPI()




#TODO: Check MCP list & status
@core.get()
async def check_list():
    pass



#TODO: Create MCP Server
@core.post()
async def create_mcp_server():
    pass



#TODO: Control MCP Servers
@core.post()
async def control_mcp_server():
    pass


from fastapi import FastAPI
import uvicorn


core = FastAPI()

db_handler = DBHandler()




#TODO: Check MCP list & status
@core.get("/manager/check_list")
async def check_list():
    # Check list of all mcp servers



    # Check status of mcp servers


    pass



#TODO: Create MCP Server
@core.post("manager/create_mcp_server")
async def create_mcp_server(mcp_schema):
    pass



#TODO: Control MCP Servers
@core.post("manager/control_mcp_server")
async def control_mcp_server(control_params):
    pass



if __name__ == "__main__":
    uvicorn.run(core)
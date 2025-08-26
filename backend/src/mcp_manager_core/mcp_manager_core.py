from handlers.database_handler import DBHandlerPG, DBHandlerRDS
from handlers.container_handler import DockerHandler
from handlers.utils.schemas import MCPSchema
from fastapi import FastAPI
import uvicorn


core = FastAPI()

db_handler_pg = DBHandlerPG()
db_handler_rds = DBHandlerRDS()
docker_handler = DockerHandler()




# TODO: Check MCP list
@core.get("/manager/check_list")
async def check_list():
    # TODO: Check list of all mcp servers
    pass


# TODO: Check MCP status
@core.get("/manager/check_status")
async def check_status():
    # TODO: Check status of mcp servers
    pass


# TODO: Create MCP Server
@core.post("manager/create_mcp_server")
async def create_mcp_server(mcp_schema:MCPSchema):
    # TODO: Create mcp server
    docker_handler.create(mcp_schema.tag, mcp_schema.port)


    # TODO: Register into the dbs.
    pass



# TODO: Control MCP Servers
@core.post("manager/control_mcp_server")
async def control_mcp_server(control_params):
    pass



if __name__ == "__main__":
    uvicorn.run(core)
from handlers.database_handler import DBHandlerPG, DBHandlerRDS
from handlers.container_handler import DockerHandler
from handlers.utils.schemas import MCPSchema, MCPControlSchema
from fastapi import FastAPI
import uvicorn


core = FastAPI()

db_handler_pg = DBHandlerPG()
db_handler_rds = DBHandlerRDS()
docker_handler = DockerHandler()






# TODO: Create MCP Server
@core.post("manager/create_mcp_server")
async def create_mcp_server(mcp_schema:MCPSchema):
    # TODO: Create mcp server
    container_info = docker_handler.create()


    # TODO: Register into the dbs.
    db_handler_rds.db_insert()






# TODO: Check MCP list
@core.get("/manager/check_list")
async def check_list():
    # TODO: Check list of all mcp servers
    pass





# TODO: Check MCP status
@core.get("/manager/check_status")
async def check_status():    # TODO: Check status of mcp servers
    pass



##########################################################################################################################





# TODO: Control MCP Servers
@core.post("manager/control_mcp_server")
async def control_mcp_server(control_params: MCPControlSchema):
    match control_params.controlCommand:
        case "pause":
            docker_handler.pause(contID=control_params.serverId)
        case "delete":
            docker_handler.delete(contID=control_params.serverId)
        case "restart":
            docker_handler.restart(contID=control_params.serverId)
        case "edit":
            # TODO: Edit için docker fonksiyonu oluştur. [Opsiyonel]
            pass













##########################################################################################################################







if __name__ == "__main__":
    uvicorn.run(core)
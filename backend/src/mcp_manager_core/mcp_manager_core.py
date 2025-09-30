from handlers.database_handler import DBHandlerPG, DBHandlerRDS
from handlers.container_handler import DockerHandler
from handlers.utils.schemas import MCPControlSchema, MCPCreateSchema, PGItem

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, status
import uvicorn


core = FastAPI()

core.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

db_handler_pg = DBHandlerPG()
db_handler_rds = DBHandlerRDS()
docker_handler = DockerHandler()


# TODO: Redis için bütün mcp server listesi init scripti ile sql db'den alınacak




# Create MCP Server
@core.post("/manager/create_mcp_server", status_code=status.HTTP_200_OK)
async def create_mcp_server(mcp_schema:MCPCreateSchema):
    """create_mcp_server"""

    # Create docker container
    container_id, container_port = docker_handler.create(fname=mcp_schema.server_name, 
                                                         ftype=mcp_schema.servertype,
                                                         fpkgs=mcp_schema.pkgs,
                                                         fargs=mcp_schema.func_args, 
                                                         fbody=mcp_schema.func_body, 
                                                         tag=f"{mcp_schema.server_name.lower()}:latest")

    # Create redis entry 
    redis_entry = {
        "container_id": container_id,
        "server_name": mcp_schema.server_name,
        "server_status": "active",
        "server_port": container_port
    }

    db_handler_rds.db_insert(contId=container_id, contInfo=redis_entry)

    # Create postgresql entry
    pg_entry = PGItem(
        container_id= container_id,
        server_port= container_port,
        mcp_server_name= mcp_schema.server_name,
        mcp_server_description= mcp_schema.description,
        function_args= db_handler_pg.args_to_dict(mcp_schema.func_args),
        function_body= mcp_schema.func_body
    )

    db_handler_pg.db_insert(pg_entry=pg_entry)



    # TODO: Register description into the vector db.

    # TODO: Register into path table eg: "*://manager/path/{funtion_name}".



# TODO: Check MCP list
@core.get("/manager/check_list")
async def check_list():
    """check_list"""
    # TODO: Check list of all mcp servers
    # TODO: Liste kontrolü SQL db'den yapılacak
    pass




# Check MCP status
@core.get("/manager/check_status")
async def check_status():
    """check_status"""
    # Check status of mcp servers
    stat_list = db_handler_rds.db_read_all_status()

    return {"status": stat_list}



# Control MCP Servers
@core.post("/manager/control_mcp_server", status_code=status.HTTP_200_OK)
async def control_mcp_server(control_params: MCPControlSchema):
    try:
        match control_params.controlCommand:
            case "pause":
                docker_handler.pause(contID=control_params.serverId)
                
                # Update redis status
                db_handler_rds.db_update(contId=control_params.serverId, status_entry="paused")

            case "delete":
                docker_handler.delete(contID=control_params.serverId)
                
                # Delete redis entry
                db_handler_rds.db_delete(contId=control_params.serverId)

                # Delete postgresql entry
                db_handler_pg.db_delete(contID=control_params.serverId)


            case "restart":
                # Container restart
                docker_handler.restart(contID=control_params.serverId)

                # Redis status update
                db_handler_rds.db_update(contId=control_params.serverId, status_entry="active")

    except Exception as e:
        raise e





if __name__ == "__main__":
    uvicorn.run("mcp_manager_core:core", host="localhost", port=8000)
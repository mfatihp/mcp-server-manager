from handlers.database_handler import DBHandlerPG, DBHandlerRDS
from handlers.container_handler import DockerHandler
from handlers.utils.schemas import MCPSchema, MCPControlSchema, MCPCreateSchema

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn


core = FastAPI()

core.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# db_handler_pg = DBHandlerPG()
db_handler_rds = DBHandlerRDS()
docker_handler = DockerHandler()


# TODO: Redis için bütün mcp server listesi init scripti ile sql db'den alınacak




# TODO: Create MCP Server
@core.post("/manager/create_mcp_server")
async def create_mcp_server(mcp_schema:MCPCreateSchema):
    redis_entry = {
        "server_name": mcp_schema.server_name,
        "description": mcp_schema.description,
        "server_type": mcp_schema.servertype,
        "pkgs":mcp_schema.pkgs,
        "func_args": mcp_schema.func_args,
        "func_body": mcp_schema.func_body,
    }

    # TODO: Paket isimlerinin yükleme komutları için db table kurulacak veya otomatik olarak pypi'den çekilecek

    print(redis_entry)

    container_info = docker_handler.create(fname=mcp_schema.server_name, 
                                           ftype=mcp_schema.servertype,
                                           fpkgs=mcp_schema.pkgs,
                                           fargs=mcp_schema.func_args, 
                                           fbody=mcp_schema.func_body, 
                                           tag=f"{mcp_schema.server_name.lower()}:latest", 
                                           port=50001)

    # TODO: Register into the dbs.
    db_handler_rds.db_insert(contId=container_info, contInfo=redis_entry)

    # TODO: Register description into the vector db.

    # TODO: Register into path table eg: "*://manager/path/{funtion_name}".






# TODO: Check MCP list
@core.get("/manager/check_list")
async def check_list():
    # TODO: Check list of all mcp servers
    # TODO: Liste kontrolü SQL db'den yapılacak
    pass





# TODO: Check MCP status
@core.get("/manager/check_status")
async def check_status():    
    # TODO: Check status of mcp servers
    # TODO: Status kontrolü redis db'den yapılacak
    pass



##########################################################################################################################





# TODO: Control MCP Servers
@core.post("manager/control_mcp_server")
async def control_mcp_server(control_params: MCPControlSchema):
    match control_params.controlCommand:
        case "pause":
            docker_handler.pause(contID=control_params.serverId)
            # TODO: Update redis status

        case "delete":
            docker_handler.delete(contID=control_params.serverId)
            
            # TODO: Delete redis entry
            db_handler_rds.db_delete(contId=control_params.serverId)

            # TODO: Delete postgresql entry

            # TODO: Return signal for delete process

        case "restart":
            docker_handler.restart(contID=control_params.serverId)

        case "edit":
            # TODO: Edit için docker fonksiyonu oluştur. [Opsiyonel]
            pass













##########################################################################################################################







if __name__ == "__main__":
    uvicorn.run("mcp_manager_core:core", host="localhost", port=8000)
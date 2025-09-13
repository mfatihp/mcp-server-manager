from pydantic import BaseModel
from typing import List, Optional




class MCPSchema(BaseModel):
    name:str
    tag:str
    port:str


class ControlParams(BaseModel):
    server_name: Optional[str]
    description: Optional[str]
    func: Optional[str]
    servertype: Optional[str]


class MCPControlSchema(BaseModel):
    serverId: str
    controlCommand: str
    controlParams: List[ControlParams]
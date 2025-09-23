from pydantic import BaseModel
from typing import List, Optional, Dict




class MCPSchema(BaseModel):
    name:str
    tag:str
    port:str


class MCPCreateSchema(BaseModel):
    server_name: str
    description: str
    servertype: str
    pkgs: List[str]
    func_args: str
    func_body: str


class ControlParams(BaseModel):
    server_name: Optional[str]
    description: Optional[str]
    func: Optional[str]
    servertype: Optional[str]


class MCPControlSchema(BaseModel):
    serverId: str
    controlCommand: str
    controlParams: Optional[Dict[str, ControlParams]]
from pydantic import BaseModel
from typing import List, Optional, Dict
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base


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
    controlParams: Optional[Dict[str, ControlParams]] = None


class PGItem(BaseModel):
    container_id: str
    server_port: str
    mcp_server_name: str
    mcp_server_description: str
    function_args: Dict[str, str]
    function_body: str


class RDSItem(BaseModel):
    container_id: str
    server_name: str
    server_status: str
    server_port: str


## ORM Models

Base = declarative_base()

class PGItemORM(Base):
    __tablename__ = "mcp_servers"
    id = Column(Integer, primary_key=True)
    container_id = Column(String)
    server_port = Column(String)
    mcp_server_name = Column(String)
    mcp_server_description = Column(String)
    function_args = Column(JSONB)
    function_body = Column(Text)
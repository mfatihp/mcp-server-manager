from pydantic import BaseModel




class MCPSchema(BaseModel):
    name:str
    tag:str
    port:str


class MCPControlSchema(BaseModel):
    serverName: str
    controlType: str
from pydantic import BaseModel




class MCPSchema(BaseModel):
    name:str
    tag:str
    port:str
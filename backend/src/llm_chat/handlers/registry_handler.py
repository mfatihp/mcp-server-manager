from pydantic import BaseModel
from typing import List, Dict



class ToolModel(BaseModel):
    server_port: str
    # tool_type:   str
    description: str = ""
    args:        Dict[str, str] = {}
    # returns: List[str] = []


class FunctionRegistry(BaseModel):
    functions: Dict[str, Dict[str, str]] = {}
    routes:    Dict[str, str] = {}

    class Config:
        extra = "allow" 

    def add_function(self, name: str, args: List[str] = None):
        """Add a single function"""
        self.functions[name] = ToolModel(args=args or [])

    
    def bulk_add(self, func_data: List[Dict[str, List[str]]]):
        for item in func_data:
            name = item["mcp_server_name"]
            
            new_tmodel = ToolModel(
                server_port=item["server_port"],
                description=item["mcp_server_description"],
                args=item["function_args"],
            )

            self.routes[name] = item["server_port"]
            self.functions[name] = new_tmodel.model_dump_json()
        

    def to_json(self, indent: int = 4):
        return self.model_dump_json(indent=indent)

from pydantic import BaseModel
from typing import List, Dict



class ToolModel(BaseModel):
    description: str = ""
    args: List[str] = []
    returns: List[str] = []


class FunctionRegistry(BaseModel):
    functions: Dict[str, ToolModel] = {}

    def add_function(self, name: str, args: List[str] = None):
        """Add a single function"""
        self.functions[name] = ToolModel(args=args or [])

    
    def bulk_add(self, func_data: List[Dict[str, List[str]]]):
        for item in func_data:
            name = item["name"]
            args = item.get("args", [])
            self.add_function(name, args)
        

    def to_json(self, indent: int = 4):
        return self.model_dump_json(indent=indent)




if __name__ == "__main__":
    flist = FunctionRegistry()
    flist.add_function("func1", ["arg1", "arg2"])
    print(flist.to_json())
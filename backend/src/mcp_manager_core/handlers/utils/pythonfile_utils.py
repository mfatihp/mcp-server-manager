from jinja2 import Environment, FileSystemLoader
import textwrap




def create_tool_file(function_name:str="ocaptai",
                     function_type:str="tool", 
                     func_args:str="a: int, b:int", 
                     func_body:str="   return a + b"):
    
    env = Environment(loader=FileSystemLoader("../mcp_server_template/python_templates/"))
    template = env.get_template("mcp_tool_template.py.j2")

    pythonfile_content = template.render(
        name=function_name,
        o_type=function_type,
        mcp_function = textwrap.dedent(f"""
        def {function_name}({func_args}):
        {func_body}
        """)
    )

    with open("../mcp_server_template/mcp.py", "w") as f:
        f.write(pythonfile_content)
    

def create_requirements_file():
    pass
    



if __name__ == "__main__":
    create_tool_file(function_name="Hello_world")
from jinja2 import Environment, FileSystemLoader
from typing import List
import textwrap

from handlers.data.pip_pkg_list import pkg_list


def create_tool_file(function_name:str="ocaptai",
                     function_type:str="tool",
                     function_desc:str="",
                     func_args:str="a: int, b:int", 
                     func_body:str="   return a + b"):
    
    env = Environment(loader=FileSystemLoader("../mcp_server_template/python_templates/"))
    template = env.get_template("mcp_tool_template.py.j2")

    pythonfile_content = template.render(
        name=function_name,
        docstr=function_desc,
        o_type=function_type,
        f_args=func_args,
        mcp_function = textwrap.dedent(f"""
        {func_body}
        """)
    )

    with open("../mcp_server_template/mcp.py", "w") as f:
        f.write(pythonfile_content)
    

def create_requirements_file(pkgs: List):
    env = Environment(loader=FileSystemLoader("../mcp_server_template/requirements_templates/"))
    template = env.get_template("user_requirements.txt.j2")

    required_cmds = [pkg_list[i] for i in pkgs]

    requirements_content = template.render(
        requirements=required_cmds
    )

    with open("../mcp_server_template/user_requirements.txt", "w") as f:
        f.write(requirements_content)
    



if __name__ == "__main__":
    create_tool_file(function_name="Hello_world")
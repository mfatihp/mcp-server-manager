from jinja2 import Environment, FileSystemLoader
import textwrap




def create_tool_file(function_name:str="ocaptai"):
    env = Environment(loader=FileSystemLoader("src/mcp_server_template/python_templates"))
    template = env.get_template("mcp_tool_template.py.j2")

    pythonfile_content = template.render(
        name=function_name,
        o_type="resource",
        mcp_function = textwrap.dedent(f"""
        def {function_name}(a, b):
            return a + b
        """)
    )

    with open("src/mcp_server_template/mcp.py", "w") as f:
        f.write(pythonfile_content)
    

    




if __name__ == "__main__":
    create_tool_file(function_name="OcaptainMycaptain")
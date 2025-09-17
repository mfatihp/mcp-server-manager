from jinja2 import Environment, FileSystemLoader



def create_dockerfile(base_image="python:3.12.11-bookworm", 
                      packages=None, 
                      tool_name=None, 
                      port=None, 
                      project_files=".",
                      requirements=False) -> None:
    
    env = Environment(loader=FileSystemLoader("../mcp_server_template/dockerfile_templates"))
    template = env.get_template("Dockerfile.j2")

    dockerfile_content = template.render(
        requirements=requirements,
        base_image=base_image,
        packages=packages,
        expose_port=port,
        project_files=project_files,
        tool_name=tool_name
    )


    with open("../mcp_server_template/Dockerfile", "w") as f:
        f.write(dockerfile_content)
from jinja2 import Environment, FileSystemLoader



def create_dockerfile(base_image="python:3.11-slim", 
                      packages=None, 
                      command=None, 
                      port=None, 
                      project_files=".") -> None:
    
    env = Environment(loader=FileSystemLoader("src/mcp_server_template/dockerfile_templates"))
    template = env.get_template("Dockerfile.j2")

    command = command

    dockerfile_content = template.render(
        base_image=base_image,
        packages=packages,
        expose_port=port,
        project_files=project_files,
        command=command
    )


    with open("test.Dockerfile", "w") as f:
        f.write(dockerfile_content)
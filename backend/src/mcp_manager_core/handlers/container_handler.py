import docker
from dotenv import dotenv_values




class DockerHandler:
    def __init__(self):
        env_values = dotenv_values("src/mcp_manager_core/.env")
        self.docker_cli = docker.DockerClient(base_url=env_values["DOCKER_URL"])


    def pause(self):
        pass


    def delete(self):
        pass

    
    def restart(self):
        pass
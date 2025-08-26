import docker
from dotenv import dotenv_values




class DockerHandler:
    def __init__(self):
        env_values = dotenv_values("src/mcp_manager_core/.env")
        self.docker_cli = docker.DockerClient(base_url=env_values["DOCKER_URL"])
    

    def create(self, tag, port):
        try:
            self.docker_cli.images.build(path="", tag=tag, rm=True)

            self.docker_cli.containers.run(image=tag, name="", detach=True, ports=port)

        except Exception:
            raise "Something is not right"



    def pause(self, contID:str):
        self.docker_cli.containers.get(container_id=contID).pause()


    def restart(self, contID:str):
        self.docker_cli.containers.get(container_id=contID).restart()


    def delete(self, contID:str):
        self.docker_cli.containers.get(container_id=contID).kill()

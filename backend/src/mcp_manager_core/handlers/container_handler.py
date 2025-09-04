import docker
from dotenv import dotenv_values
from utils.pythonfile_utils import create_tool_file
from utils.docker_utils import create_dockerfile



class DockerHandler:
    def __init__(self):
        env_values = dotenv_values("src/mcp_manager_core/.env")
        self.docker_cli = docker.DockerClient(base_url=env_values["DOCKER_URL"])
    

    def create(self, fname, tag, port):
        try:
            create_tool_file(function_name=fname)
            create_dockerfile(port=8000)

            self.docker_cli.images.build(path="src/mcp_server_template/", tag=tag, rm=True)

            # self.docker_cli.containers.run(image=tag, name="", detach=True, ports=port)

        except Exception as e:
            raise e



    def pause(self, contID:str):
        self.docker_cli.containers.get(container_id=contID).pause()


    def restart(self, contID:str):
        self.docker_cli.containers.get(container_id=contID).restart()


    def delete(self, contID:str):
        self.docker_cli.containers.get(container_id=contID).kill()




if __name__ == "__main__":
    dh = DockerHandler()
    dh.create(fname="wow", tag="wow:1.0.0", port="8000")
import docker
from dotenv import dotenv_values
from handlers.utils.pythonfile_utils import create_tool_file, create_requirements_file
from handlers.utils.docker_utils import create_dockerfile



class DockerHandler:
    def __init__(self):
        env_values = dotenv_values(".env")
        self.docker_cli = docker.DockerClient(base_url=env_values["DOCKER_URL"])
    

    def create(self, fname, ftype, fargs, fbody, fpkgs, tag, port):
        # try:
        create_tool_file(function_name=fname,
                            function_type=ftype,
                            func_args=fargs,
                            func_body=fbody)
        
        create_dockerfile(tool_name=fname,
                            port=port)
        
        create_requirements_file(pkgs=fpkgs)

        self.docker_cli.images.build(path="../mcp_server_template/", tag=tag, rm=True)

        container = self.docker_cli.containers.run(image=tag, name=f"mcp_{fname.lower()}", detach=True,  ports={"50001/tcp": 50001})

        # TODO: Docker ile otomatik port ataması yapılacak.
        container.reload()
        # print(container.attrs)

        container_port = container.attrs['NetworkSettings']['Ports']['50001/tcp'][0]['HostPort']
        print(container_port)
        
        return container_port

        # except Exception as e:
        #     raise e



    def pause(self, contID:str):
        self.docker_cli.containers.get(container_id=contID).pause()


    def restart(self, contID:str):
        self.docker_cli.containers.get(container_id=contID).restart()


    def delete(self, contID:str):
        self.docker_cli.containers.get(container_id=contID).kill()




if __name__ == "__main__":
    dh = DockerHandler()
    dh.create(fname="wow", tag="wow:1.0.0", port="8000")
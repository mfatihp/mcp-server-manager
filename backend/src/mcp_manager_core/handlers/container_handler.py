import docker
from dotenv import dotenv_values
from handlers.utils.pythonfile_utils import create_tool_file, create_requirements_file
from handlers.utils.docker_utils import create_dockerfile



class DockerHandler:
    def __init__(self):
        env_values = dotenv_values(".env")
        self.docker_cli = docker.DockerClient(base_url=env_values["DOCKER_URL"])
    

    def create(self, fname, ftype, fargs, fbody, fpkgs, tag, port=50001):
        try:
            create_tool_file(function_name=fname,
                            function_type=ftype,
                            func_args=self.arg_seperator(fargs),
                            func_body=fbody)
            
            create_dockerfile(tool_name=fname,
                            port=port)
            
            create_requirements_file(pkgs=fpkgs)

            self.docker_cli.images.build(path="../mcp_server_template/", tag=tag, rm=True)

            container = self.docker_cli.containers.run(image=tag, name=f"mcp_{fname.lower()}", detach=True,  ports={f"{port}/tcp": None})

            container.reload()

            container_port = container.attrs['NetworkSettings']['Ports'][f'{port}/tcp'][0]['HostPort']
            container_id = container.id
            
            return container_id, container_port

        except Exception as e:
            raise e


    def unpause(self, contID:str):
        self.docker_cli.containers.get(container_id=contID).unpause()

    def pause(self, contID:str):
        self.docker_cli.containers.get(container_id=contID).pause()

    def restart(self, contID:str):
        self.docker_cli.containers.get(container_id=contID).restart()

    def delete(self, contID:str):
        self.docker_cli.containers.get(container_id=contID).kill()
    
    @staticmethod
    def arg_seperator(arg:str):
        a = arg.split(",")
        b = [i.split(":")[0].strip() for i in a]
        c = str(b).replace("[", "").replace("]", "").replace("'", "")
        
        return c




if __name__ == "__main__":
    s = "x: int, y: int"
    a = s.split(",")
    b = [i.split(":")[0].strip() for i in a]
    c = str(b).replace("[", "").replace("]", "").replace("'", "")

    print(c)
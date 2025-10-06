import requests




class LlmHandler:
    def __init__(self):
        # Model Init
        pass


    def response(self, prompt:str):
        # 1. Detect Tool request
        context = "<------ Prompt will be here ------> Return OK or Not"

        if context == "OK":
        # 2. If Tool OK call mcp_request
            pass
        else:
        # 3. Else return model response with no tool use info
            pass


    def check_tool_list(self):
        # Check possible functions by descriptions
        pass


    def mcp_request(self):
        # Tool or Resource call
        pass


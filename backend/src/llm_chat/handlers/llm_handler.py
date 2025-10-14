from transformers import AutoModelForCausalLM, AutoTokenizer
from utils import llm_pipe
from db_handler import DBHandlerPG
from registry_handler import FunctionRegistry
import requests
import os

from dotenv import dotenv_values




class LlmHandler(DBHandlerPG, FunctionRegistry):
    def __init__(self):
        super().__init__()
        # Model Init
        env_values = dotenv_values("../.env")
        model_name = env_values["MODEL_NAME"]

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, 
                                                          dtype="auto",
                                                          device_map="auto")
        
        self.instruct = """
                        You are a chat that use external functions. When you receive an input from user,check the function list below, 
                        if user message contains or mention a function, return JSON output using following format and do not use any spaces:
                        {"need_mcp":"OK", "answer":"", "function_name": <function_name>, "args": <["arg1", "arg2", etc.]>}

                        if user not contain a request create an answer in following format and do not use any spaces and replace your answer 
                        in place of "<Insert Your Answer Here>":
                        {"need_mcp":"NOK", "answer":<Insert Your Answer Here>, "function_name":"", "args": []}

                        Function list is below:
                        """
        
        self.model_config = {
            "instruction": self.instruct,
            "tokenizer": self.tokenizer,
            "model": self.model
        }


    def response(self, prompt:str):
        # TODO: Ensure mcp config list is converted to string
        # db_result = self.check_db()
        # func_info = self.bulk_add(db_result)

        # Update tool pool
        # 1. Detect Tool request
        context = llm_pipe(prompt=prompt, model_config=self.model_config)
        print(context)

        # if context == "OK":
        # # 2. If Tool OK call mcp_request
        #     result = self.mcp_request()
        # else:
        # # 3. Else return model response with no tool use info
        #     pass


    def check_tool_list(self):
        # Check possible functions by descriptions
        pass


    def mcp_request(self, request:str):
        # Tool or Resource call
        pass



if __name__ == "__main__":
    t = LlmHandler()
    t.response("Calculate 1 + 1")
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
        
        self.instruction = """
                            You are a function-aware chat assistant. You can analyze user messages and decide whether a function call is needed 
                            based on the function list provided below.

                            When you receive a message:
                            1. Check if the user's input explicitly mentions or implies the use of any function from the list.
                            2. If a function should be used:
                            - Return a compact JSON object **with no extra spaces or line breaks** in the following format:
                                {"need_mcp":"OK","answer":"","function_name":"<function_name>","args":["<arg1>","<arg2>",...]}
                            3. If no function is relevant:
                            - Return a compact JSON object **with no extra spaces or line breaks** in the following format:
                                {"need_mcp":"NOK","answer":"<Insert your natural language answer here>","function_name":"","args":[]}

                            Important rules:
                            - Do not add explanations, formatting, or text outside of the JSON object.
                            - Preserve JSON syntax strictly (no trailing commas, no missing quotes).
                            - Match function names and argument positions exactly as defined.
                            - Always output either "OK" or "NOK" in the "need_mcp" field.
                            - Never include extra whitespace anywhere in the output.

                            Function list:
                            """
        
        self.model_config = {
            "instruction": self.instruction,
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
from transformers import AutoModelForCausalLM, AutoTokenizer
from handlers.utils import llm_pipe
import requests
import os

from dotenv import dotenv_values




class LlmHandler:
    def __init__(self):
        # Model Init
        env_values = dotenv_values("llm_chat/.env")
        model_name = env_values("MODEL_NAME")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, 
                                                          torch_dtype="auto",
                                                          device_map="auto")
        
        self.tools = {
            "tokenizer": self.tokenizer,
            "model": self.model
        }


    def response(self, prompt:str):
        # Update tool pool
        # 1. Detect Tool request
        context = llm_pipe(prompt=prompt, tools=self.tools, check_mcp=True)

        if context == "OK":
        # 2. If Tool OK call mcp_request
            result = self.mcp_request()
        else:
        # 3. Else return model response with no tool use info
            pass


    def check_tool_list(self):
        # Check possible functions by descriptions
        pass


    def mcp_request(self, request:str):
        # Tool or Resource call
        pass
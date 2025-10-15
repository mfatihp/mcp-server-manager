from transformers import AutoModelForCausalLM, AutoTokenizer
from utils import llm_pipe
from db_handler import DBHandlerPG
from registry_handler import FunctionRegistry
import requests
import os

from dotenv import dotenv_values




class LlmHandler(DBHandlerPG):
    def __init__(self):
        super().__init__()
        self.registry = FunctionRegistry()
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


    def response(self, user_prompt:str):
        # TODO: Ensure mcp config list is converted to string
        db_result = self.check_db()
        self.registry.bulk_add(db_result)

        # Update tool pool
        # 1. Detect Tool request
        context = self.llm_pipe(prompt=user_prompt)
        print(context)

        if context["need_mcp"] == "OK":
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

    def llm_pipe(self, prompt: str, func_json: str={}):
    
        messages = [
                {"role": "system", "content": f"""{self.instruction}\n
                                                  {func_json}"""},
                {"role": "user", "content": prompt}
                ]
        print(messages[0])
            
        text = self.tokenizer.apply_chat_template(messages,
                                                  tokenize=False,
                                                  add_generation_prompt=True)
        
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        generated_ids = self.model.generate(**model_inputs, max_new_tokens=16384)
        output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 
        content = self.tokenizer.decode(output_ids, skip_special_tokens=True)

        return content



if __name__ == "__main__":
    t = LlmHandler()
    #print(LlmHandler.__mro__)
    t.response("Calculate 1 + 1")
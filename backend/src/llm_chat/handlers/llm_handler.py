from transformers import AutoModelForCausalLM, AutoTokenizer
from db_handler import DBHandlerPG
from registry_handler import FunctionRegistry
import json
import requests

from dotenv import dotenv_values




class LlmHandler(DBHandlerPG):
    def __init__(self):
        super().__init__()
        self.registry = FunctionRegistry()
        
        # Model Init
        env_values = dotenv_values("../.env")
        model_name = env_values["MODEL_NAME"]

        self.tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, 
                                                          dtype="auto",
                                                          device_map="auto", 
                                                          local_files_only=True)
        
        self.instruction = """
                            You are a function-aware chat assistant. You can analyze user messages and decide whether a function call is needed 
                            based on the function list provided below.

                            When you receive a message:
                            1. Check if the user's input explicitly mentions or implies the use of any function from the list.
                            2. If a function should be used:
                            - Return a compact JSON object **with no extra spaces or line breaks** in the following format:
                                {"need_mcp":"OK","answer":"","function_name":"<function_name>","args":{"<arg1 name>":"<arg1>","<arg2 name>":"<arg2>",...},"arg_types":{""<arg1 name>":<arg1 type>","<arg2 name>":"<arg2 type>",...}}
                            3. If no function is relevant:
                            - Return a compact JSON object **with no extra spaces or line breaks** in the following format:
                                {"need_mcp":"NOK","answer":"<Insert your natural language answer here>","function_name":"","args":{},"arg_types":{}}

                            Important rules:
                            - Do not add explanations, formatting, or text outside of the JSON object.
                            - Preserve JSON syntax strictly (no trailing commas, no missing quotes).
                            - Match function names and argument positions exactly as defined.
                            - Always output either "OK" or "NOK" in the "need_mcp" field.
                            - Never include extra whitespace anywhere in the output.

                            Function list:
                            """
        
        self.instruction_2 = """
                            You are a response synthesizer that combines user requests with external data.

                            Inputs you receive:
                            1. user_message — what the user originally asked.
                            2. mcp_response — the structured data or result returned by an external function.

                            Your goal:
                            - Use the mcp_response to create a helpful and natural-language answer to the user.
                            - The answer should sound like a normal chat reply, not just raw data.
                            - Avoid mentioning technical details about MCP, JSON, or functions.

                            Output format:
                            Return a single compact JSON object (no extra spaces or line breaks):
                            {"final_answer":"<Your complete, natural-language answer to the user>"}

                            Rules:
                            - Make the answer short, polite, and clear (for example: “The result is 2.” instead of just “2”).
                            - You can include short context like “Here’s the result…” or “That equals…” if appropriate.
                            - Never add extra formatting or text outside the JSON object.
                            """
        
        self.model_config = {
            "instruction": self.instruction,
            "tokenizer": self.tokenizer,
            "model": self.model
        }

        self.latest_prompt = ""


    def response(self, user_prompt:str):
        self.latest_prompt = user_prompt
        db_result = self.check_db()

        self.registry.bulk_add(db_result)

        # Update tool pool
        # 1. Detect Tool request
        context = self.llm_pipe(func_json=self.registry.functions)

        if context["need_mcp"] == "OK":
        # 2. If Tool OK call mcp_request
            mcp_answer = self.mcp_request(context=context)
            result = self.llm_pipe(enhance_msg=mcp_answer)

            # print(result)
            return result["final_answer"]
        else:
        # 3. Else return model response with no tool use info
            return context["answer"]
            # print(context["answer"])


    def mcp_request(self, context:dict):
        # Tool or Resource call
        func_url = f"http://localhost:{self.registry.routes[context["function_name"]]}/{context["function_name"]}"

        type_map = {
            "int": int,
            "float": float,
            "str": str,
            "bool": lambda v: v.lower() in ("true", "1", "yes")
        }

        converted = {k: type_map[context["arg_types"][k]](v) for k, v in context["args"].items()}

        resp = requests.post(url=func_url, json=converted)

        return resp.json()

        # TODO: URI ayarlaması yapılacak veya tool - resource ayrımı için lojik kurulacak.


    def llm_pipe(self, func_json:str = None, enhance_msg:dict = None):
        if enhance_msg == None:
            messages = [
                    {"role": "system", "content": f"""{self.instruction}\n
                                                      {func_json}"""},
                    {"role": "user", "content": self.latest_prompt}
                    ]
        else: 
            messages = [
                    {"role": "system", "content": f"""{self.instruction_2}"""},
                    {"role": "user", "content": f"User message: {self.latest_prompt}\nMCP response: {enhance_msg}"}
                    ]
            
        text = self.tokenizer.apply_chat_template(messages,
                                                  tokenize=False,
                                                  add_generation_prompt=True)
        
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        generated_ids = self.model.generate(**model_inputs, max_new_tokens=16384)
        output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 
        content = self.tokenizer.decode(output_ids, skip_special_tokens=True)

        return json.loads(content)



if __name__ == "__main__":
    t = LlmHandler()
    t.response("What is result of 3 plus 7?")
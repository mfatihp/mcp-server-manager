instructions = """
        You are a chat that use external functions. When you receive an input from user,check the function list below, 
        if user message contains or mention a function, return JSON output using following format:
        {\
                "need_mcp":"OK",
                "answer":"",
                "function_name":"function_name"
                "args": ["arg1", "arg2", etc.]
        }
        if user not contain a request create an answer in following format:
        {\
                "need_mcp":"NOK",
                "answer":"YOU SHALL NOT PASS",
                "function_name":""
                "args": []
        }

        Function list is below:
"""







def llm_pipe(prompt: str, tools: dict, func_json: str, instruct: str):
    
    messages = [
            {"role": "system", "content": f"""{instruct}\n
                                              {func_json}"""},
            {"role": "user", "content": prompt}
            ]
        
    text = tools["tokenizer"].apply_chat_template(messages,
                                                  tokenize=False,
                                                  add_generation_prompt=True)
    
    model_inputs = tools["tokenizer"]([text], return_tensors="pt").to(tools["model"].device)
    generated_ids = tools["model"].generate(**model_inputs, max_new_tokens=16384)
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 
    content = tools["tokenizer"].decode(output_ids, skip_special_tokens=True)

    return {"content:": content}




if __name__ == "__main__":
    from transformers import pipeline

    pipe = pipeline("text-generation", "Qwen3/Qwen3-4B-Instruct-2507-FP8")

    result = pipe("Hello")

    print(result)




def llm_pipe(prompt: str, model_config: dict, func_json: str={}):
    
    messages = [
            {"role": "system", "content": f"""{model_config["instruction"]}\n
                                              {func_json}"""},
            {"role": "user", "content": prompt}
            ]
        
    text = model_config["tokenizer"].apply_chat_template(messages,
                                                  tokenize=False,
                                                  add_generation_prompt=True)
    
    model_inputs = model_config["tokenizer"]([text], return_tensors="pt").to(model_config["model"].device)
    generated_ids = model_config["model"].generate(**model_inputs, max_new_tokens=16384)
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 
    content = model_config["tokenizer"].decode(output_ids, skip_special_tokens=True)

    return content












if __name__ == "__main__":
    from transformers import pipeline
    from huggingface_hub import login

    pipe = pipeline("text-generation", "Qwen/Qwen3-4B-Instruct-2507-FP8")

    result = pipe("Hello, how can i use you?")

    print(result)


def llm_pipe(prompt: str, tools: dict):
    
    messages = [
            {"role": "system", "content": ""},
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
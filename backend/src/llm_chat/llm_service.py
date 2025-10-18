from handlers.llm_handler import LlmHandler
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn

from huggingface_hub import login
from dotenv import load_dotenv
import os
load_dotenv()

login(token=os.getenv("HF_API_KEY"))



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"]
)


chat_bot = LlmHandler()



@app.get("/chat")
def llm_chat(prompt):
    response = chat_bot.response(prompt=prompt)

    return {"Response": response}



if __name__ == "__main__":
    uvicorn.run(app)





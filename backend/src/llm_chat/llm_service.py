from handlers.llm_handler import LlmHandler
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
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
    allow_methods=["POST"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    text: str

chat_bot = LlmHandler()



@app.post("/chat")
def llm_chat(req: ChatRequest):
    response = chat_bot.response(user_prompt=req.text)

    return {"reply": response}



if __name__ == "__main__":
    uvicorn.run(app, port=8070)





from handlers.llm_handler import LlmHandler
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI



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





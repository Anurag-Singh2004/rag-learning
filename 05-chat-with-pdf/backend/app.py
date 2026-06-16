from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str
    provider: str #groq/gemini


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    contents= await file.read()
    return {"filename": file.filename, "size": len(contents)}

@app.post("/chat")
async def chat(request: ChatRequest):
    return {"question": request.question, "provider": request.provider}
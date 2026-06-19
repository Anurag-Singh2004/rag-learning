from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from rag_pipeline import ingest_pdf, generate_answer


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
    num_chunks = ingest_pdf(contents, file.filename)
    return {"filename": file.filename, "chunks_created": num_chunks}

@app.post("/chat")
async def chat(request: ChatRequest):
    answer, num_chunks_used = generate_answer(request.question, request.provider)
    return {"answer": answer, "chunks_used": num_chunks_used}
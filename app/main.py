from fastapi import FastAPI, HTTPException
from app.gemini_client import get_azure_response
from app.schemas import QuestionRequest

app = FastAPI()

@app.get("/")
def root():
    return {"Hello": "World"}

@app.post("/ask")
async def ask(req: QuestionRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question is required")
    try:
        return get_azure_response(req.question)
    except Exception:
        raise HTTPException(status_code=502, detail="AI agent error")
from fastapi import APIRouter
from schemas import AIQueryRequest
from ai.assistant import assistant_instance

router = APIRouter(prefix="/api/ai", tags=["AI Assistant"])

@router.post("/ask")
def ask_ai(req: AIQueryRequest):
    response = assistant_instance.answer_question(req.question)
    return response

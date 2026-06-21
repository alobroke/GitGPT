from fastapi import APIRouter
from fastapi import Request

from backend.api.schemas import (
    QuestionRequest,
    QuestionResponse
)

router = APIRouter()


@router.get("/")
def health():

    return {
        "status": "running",
        "service": "GitHub Repository RAG"
    }


@router.post(
    "/ask",
    response_model=QuestionResponse
)
def ask_question(
    request: Request,
    body: QuestionRequest
):

    rag = request.app.state.rag

    result = rag.ask(
        body.question
    )

    return QuestionResponse(
        answer=result["answer"]
    )
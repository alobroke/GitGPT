from fastapi import (
    APIRouter
)

from backend.api.schemas import (
    QuestionRequest,
    QuestionResponse
)

from backend.rag.pipeline import (
    RepoRAG
)

router = APIRouter()

_loaded_rags = {}


@router.post(
    "/ask",
    response_model=QuestionResponse
)
def ask_question(
    body: QuestionRequest
):

    repository = (
        body.repository
    )

    if repository not in _loaded_rags:

        print(
            f"Loading repository RAG: {repository}"
        )

        _loaded_rags[
            repository
        ] = RepoRAG(
            repository
        )

    rag = _loaded_rags[
        repository
    ]

    result = rag.ask(
        body.question
    )

    return QuestionResponse(
        answer=result["answer"]
    )
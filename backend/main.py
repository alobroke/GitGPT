from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.api.routes import router
from backend.rag.pipeline import RepoRAG


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Loading RepoRAG...")

    app.state.rag = RepoRAG()

    print("RepoRAG Ready")

    yield


app = FastAPI(
    title="GitHub Repository RAG",
    lifespan=lifespan
)

app.include_router(router)
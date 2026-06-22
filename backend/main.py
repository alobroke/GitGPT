from backend.api.system_routes import (
    router as system_router
)

from fastapi import FastAPI

from backend.api.routes import (
    router
)

from backend.api.index_routes import (
    router as index_router
)

app = FastAPI(
    title="GitGPT"
)

app.include_router(
    router
)

app.include_router(
    index_router
)

app.include_router(
    system_router
)
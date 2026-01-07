from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.seeds.run import run_seeds_if_enabled
from app.core.version_middleware import VersionMiddleware
from app.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        run_seeds_if_enabled()
    except Exception as e:
        print("Seed execution failed:", e)

    yield


app = FastAPI(
    title="Lucky Game Backend",
    lifespan=lifespan
)

app.add_middleware(VersionMiddleware)
app.include_router(api_router)

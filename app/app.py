from fastapi import FastAPI
from app.core.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from app.models.user_model import User
from app.api.api_v1.handlers.user import user_router  # Aqui está OK



@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).todoapp
    await init_beanie(database=client, document_models=[User])
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

@app.get("/")
async def root():
    return {"message": "API está rodando!"}

app.include_router(
    user_router,
    prefix=settings.API_V1_STR
)

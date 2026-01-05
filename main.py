from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config.database import connect_to_mongo, close_mongo_connection
from app.routers import (
    produto_router,
    cliente_router,
    compra_router,
    divida_router,
    historico_router
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(
    title="API Vendas Fiado",
    description="Sistema de gestao de vendas fiadas com controle de dividas e pagamentos",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(produto_router)
app.include_router(cliente_router)
app.include_router(compra_router)
app.include_router(divida_router)
app.include_router(historico_router)


@app.get("/")
async def root():
    return {
        "message": "API Vendas Fiado",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

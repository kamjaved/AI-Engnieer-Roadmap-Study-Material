from fastapi import FastAPI

from routers.chat import router as chat_router
from routers.responses import router as responses_router

app = FastAPI(
    title="OpenAI Service API",
    description="Production-ready GenAI backend built on OpenAI SDK",
    version="1.0.0",
)

# CUSTOM ROUTES
app.include_router(chat_router)
app.include_router(responses_router)


@app.get("/health")
def health_check():
    return {"Staus": "Ok"}

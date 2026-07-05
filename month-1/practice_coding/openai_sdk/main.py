from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI

from routers.chat import router as chat_router

# reads .env file into os.environ
load_dotenv()

client = OpenAI()

app = FastAPI(
    title="OpenAI Service API",
    description="Production-ready GenAI backend built on OpenAI SDK",
    version="1.0.0",
)

# CUSTOM ROUTES
app.include_router(chat_router)


@app.get("/health")
def health_check():
    return {"Staus": "Ok"}


response = client.chat.completions.create(
    model="gpt-4o", messages=[{"role": "user", "content": "What is 2 + 2?"}]
)

print(response)

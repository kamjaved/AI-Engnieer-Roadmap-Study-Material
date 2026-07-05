from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fast_api_traversy.middleware.timer import timing_middleware
from fast_api_traversy.routes.basic_routes import router as basic_router
from fast_api_traversy.routes.issues import router as issues_router

app = FastAPI()
# Middlewares
app.middleware("http")(timing_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Routes
app.include_router(basic_router)
app.include_router(issues_router)

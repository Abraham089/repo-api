from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from repo_api_equipo_e.routers.api import router as api_router
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()
localhost_url = os.getenv("LOCALHOST")
ip_direction_url = os.getenv("IP_DIRECTION")

origins = [
    localhost_url,
    ip_direction_url
]

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
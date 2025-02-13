from fastapi import FastAPI
# from .internal import admin
from .routers import gitea_receive

app = FastAPI()

app.include_router(gitea_receive.router)
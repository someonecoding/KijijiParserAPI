from fastapi import FastAPI
import uvicorn
from api.routers import ads


def init_routers(app: FastAPI):
    app.include_router(ads.router, prefix='/api/v1')

def create_app():
    app = FastAPI()
    init_routers(app)

    return app

app = create_app()

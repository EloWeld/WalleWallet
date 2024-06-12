from fastapi import FastAPI
import uvicorn
from app.config import settings
from app.database import engine
from app.models import Base
from app.api import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Wallet API"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

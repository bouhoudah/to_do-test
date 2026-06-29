from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Todo API", version="1.0.0")
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Todo API is running"}
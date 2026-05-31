from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="OrgBrain AI",
    version="0.1.0"
)

app.include_router(router)

@app.get("/")
def root():
    return {
        "message": "OrgBrain AI Backend Running"
    }
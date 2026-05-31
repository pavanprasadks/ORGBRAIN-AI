from fastapi import FastAPI

app = FastAPI(
    title="OrgBrain AI",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "message": "OrgBrain AI Backend Running"
    }
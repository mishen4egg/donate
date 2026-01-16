from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pathlib

app = FastAPI()

BASE_DIR = pathlib.Path(__file__).parent


@app.get("/")
async def root():
    return {"status": "ok", "message": "Server is running"}


@app.get("/overlay", response_class=HTMLResponse)
async def overlay():
    return (BASE_DIR / "overlay.html").read_text(encoding="utf-8")


@app.post("/test-donation")
async def test_donation():
    return {
        "user": "TEST",
        "amount": 50
    }

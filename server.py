from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

last_donation = None


@app.get("/donate")
def donate(user: str, amount: int, text: str = ""):
    global last_donation
    last_donation = {
        "user": user,
        "amount": amount,
        "text": text
    }
    return {"ok": True}


@app.get("/last")
def last():
    return last_donation or {}


@app.get("/overlay", response_class=HTMLResponse)
def overlay():
    return open("overlay.html", encoding="utf-8").read()

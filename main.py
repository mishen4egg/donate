from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

last_donation = None

@app.post("/donation")
def push(data: dict):
    global last_donation
    last_donation = data
    return {"ok": True}

@app.get("/donation")
def pull():
    global last_donation
    d = last_donation
    last_donation = None
    return d
add fastapi server

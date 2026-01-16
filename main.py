from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

last_donation = {
    "user": "",
    "amount": "",
    "text": ""
}

@app.post("/donate")
def donate(user: str, amount: str, text: str = ""):
    last_donation["user"] = user
    last_donation["amount"] = amount
    last_donation["text"] = text
    return {"status": "ok"}

@app.get("/overlay", response_class=HTMLResponse)
def overlay():
    return f"""
    <html>
    <body style="background: transparent; color: white; font-size: 40px;">
        <div id="donation">
            {last_donation["user"]} — {last_donation["amount"]}₽<br>
            {last_donation["text"]}
        </div>
    </body>
    </html>
    """

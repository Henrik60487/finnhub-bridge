from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import os, time

# Change these later in Render environment variables to long random strings
SECRET_TOKEN = os.environ.get("WEBHOOK_SECRET", "change-me-to-a-long-random-string")
CHATGPT_API_KEY = os.environ.get("CHATGPT_API_KEY", "")

app = FastAPI(title="Finnhub Bridge API")

STORE = {"latest_event": None, "received_at": None}

@app.post("/finnhub-webhook/{secret}")
async def finnhub_webhook(secret: str, request: Request):
    if secret != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Forbidden")
    payload = await request.json()
    STORE["latest_event"] = payload
    STORE["received_at"] = time.time()
    return JSONResponse({"status": "ok", "received_at": STORE["received_at"]})

@app.get("/latest-data")
async def get_latest_data(api_key: str = None):
    if CHATGPT_API_KEY:
        if api_key != CHATGPT_API_KEY:
            raise HTTPException(status_code=403, detail="Forbidden - invalid api_key")
    if STORE["latest_event"] is None:
        return {"status": "no_data"}
    return {"status": "ok", "received_at": STORE["received_at"], "event": STORE["latest_event"]}

@app.get("/.well-known/health")
def health():
    return {"status": "ok"}

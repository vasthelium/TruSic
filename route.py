import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, JSONResponse
from authservice import OuraAuthService

app = FastAPI()
#Config (KEEP SECRETS OUT OF GIT)
OURA_CLIENT_ID = os.getenv("OURA_CLIENT_ID", "")
if not OURA_CLIENT_ID:
    raise ValueError ("Client ID Not Recieved")
OURA_CLIENT_SECRET = os.getenv("OURA_CLIENT_SECRET", "")
if not OURA_CLIENT_SECRET:
    raise ValueError ("Client Secret not recieved")
REDIRECT_URI = os.getenv("OURA_REDIRECT_URI", "http://localhost:8000/callback")
TOKEN_URL = "https://api.ouraring.com/oauth/token"
TOKENS_PATH = ".tokens/oura_tokens.json"
scope = "personal heartrate session heart_health daily workout stress"
stored_state = None

authservice = OuraAuthService(OURA_CLIENT_ID, OURA_CLIENT_SECRET, REDIRECT_URI, 
                TOKEN_URL, TOKENS_PATH, scope)
@app.get("/authoura")
def ouraauth():
    global stored_state
    authurl, secure_token = authservice.build_auth_url()
    stored_state = secure_token
    return RedirectResponse(url=authurl)  

@app.get("/callback")
async def ouuraredirect(code:str | None = None, state: str | None = None):
    if not code:
        return JSONResponse({"error": "No code received"}, status_code=400)
    if state!=stored_state:
        return JSONResponse({"error": "Invalid state"}, status_code=400)
    tokens = await authservice.exchange_code_for_token(code)
    authservice.save_tokens(tokens)
    return {
    "ok": True,
        "message": "Tokens saved locally. You can now pull Oura data using the access token.",
        "state": state,
        "saved_to": TOKENS_PATH,
        "token_keys": list(tokens.keys()),
    }
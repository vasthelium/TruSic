import os
from urllib.parse import urlencode
import json
import httpx
import pathlib
import secrets
#compare against vndrs_auth.py in unnamed engine which is route contains logic
#approach here is route calls service -> service has the logic, authservice this file
class OuraAuthService:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, 
                 token_url: str, tokens_path: str, scope: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token_url = token_url
        self.tokens_path = tokens_path
        self.scope = scope

    def build_auth_url(self):

        secure_token = secrets.token_urlsafe()
        base = "https://cloud.ouraring.com/oauth/authorize"
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
            "state": secure_token
        }
        query = urlencode(params)
        authurl = f"{base}?{query}"
        return authurl, secure_token

    async def exchange_code_for_token(self, code: str):

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        async with httpx.AsyncClient(timeout=30) as client:
            try:
                resp = await client.post(self.token_url, data=data)
                resp.raise_for_status()
            except httpx.RequestError as e:
                raise ValueError(f"Token exchange Failed: {e}")
            except httpx.HTTPStatusError as s:
                raise ValueError(f"Token exchange failed: {s.response.status_code} - {s.response.text}")
            return resp.json()
        
    def save_tokens(self, token_payload: dict):
        os.makedirs(os.path.dirname(self.tokens_path), exist_ok=True)
        with open (self.tokens_path, "w") as f:
            json.dump(token_payload, f, indent=2)
        return True

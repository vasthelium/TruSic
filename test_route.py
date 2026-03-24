import pytest
from H1_authservice import OuraAuthService
from unittest.mock import patch
from fastapi.testclient import TestClient
from H2_route import app
import H2_route

client = TestClient(app)

def test_ouraauth():
    fake_auth_url = "http://somefakeurl"
    fake_secure_token = "abc123"
    with patch("route.authservice.build_auth_url") as mock_buildurl:
        mock_buildurl.return_value = (fake_auth_url, fake_secure_token)
        response = client.get("/authoura")
        mock_buildurl.assert_called_once_with()
    assert response.status_code == 307

def test_callback():
    code = "dummycode"
    state = "dummystate"
    with patch("route.authservice.exchange_code_for_token") as mock_exchangetoken, \
        patch("route.authservice.save_tokens") as mock_savetokens:
        mock_exchangetoken.return_value = {"access_token": "abc"}
        H2_route.stored_state = "dummystate"
        callback = client.get("/callback?code=dummycode&state=dummystate")
        mock_exchangetoken.assert_called_once_with("dummycode")
        mock_savetokens.assert_called_once_with({"access_token": "abc"})
    assert callback.status_code == 200
    assert callback.json()["ok"] is True
    

import pytest
from H1_authservice import OuraAuthService
from unittest.mock import patch

client_id = "testdummy1"
secret= "testdummy2"
redirect = "testdummy3"
url = "testdummy4"
path = "some_folder/tokens.json"
scope = "testdummy6"

@pytest.mark.asyncio
async def test_token_exchange():

    authservice = OuraAuthService(client_id, secret, redirect, 
                url, path, scope)
    
    dummydata = {
            "grant_type": "dummycode",
            "code": "dummycode",
            "redirect_uri": "http://redirect",
            "client_id": "dummyclientid",
            "client_secret": "dummysecret"
        }
    faketokendict = {"access_token": "abc"}
    with patch("authservice.httpx.AsyncClient") as mock_asyncclient:

        class FakeResponse:
            def raise_for_status(*args, **kwds):
                return None
            def json(*args, **kwds):
                return faketokendict
        mock_asyncclient.return_value.__aenter__.return_value.post.return_value = FakeResponse()
        result = await authservice.exchange_code_for_token("dummycode")
        assert result == faketokendict

        mock_asyncclient.assert_awaited_once_with(mock_asyncclient.return_value.__aenter__.return_value)
        mock_asyncclient.return_value.__aenter__.return_value.post.assert_awaited_once_with("testdummy4", data=dummydata)
    
# Test complete
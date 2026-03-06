import pytest
from ingestionservice import fetch_oura
from unittest.mock import patch
import ingestionservice

# tests check if oura-access-token is empty,. token response is recieved, get url contains what needed

def test_valueerror_fetchoura():
    ingestionservice.OURA_ACCESS_TOKEN = " "
    with pytest.raises(ValueError):
        fetch_oura()

def test_response_check():
    ingestionservice.OURA_ACCESS_TOKEN = "somedummytoken"
    fake_tokenpayload = {"somekeys": "somevalues"}

    with patch("ingestionservice.httpx.Client") as mock_client:
        class FakeResponse:
            status_code = 200
            def raise_for_status(self):
                return None
            def json(*args, **kwds):
                return fake_tokenpayload
        mock_client.return_value.__enter__.return_value.get.return_value = FakeResponse()
        result = ingestionservice.fetch_oura()
        assert result == fake_tokenpayload

def test_geturl():
    ingestionservice.OURA_ACCESS_TOKEN = "somedummytoken"
    fake_tokenpayload = {"somekeys": "somevalues"}
    with patch("ingestionservice.httpx.Client") as mock_client:
        class FakeResponse:
            status_code = 200
            def raise_for_status(self):
                return None
            def json(*args, **kwds):
                return fake_tokenpayload
        mock_client.return_value.__enter__.return_value.get.return_value = FakeResponse()
        result = ingestionservice.fetch_oura()
        args, kwargs = mock_client.return_value.__enter__.return_value.get.call_args
        cur_url = args[0]
        headers = kwargs["headers"]
        assert "api.ouraring.com/v2/usercollection/sleep" in cur_url
        assert "start_date" in cur_url
        assert "end_date" in cur_url
        assert "Authorization" in headers
        assert "Bearer" in headers["Authorization"]
        assert result == fake_tokenpayload
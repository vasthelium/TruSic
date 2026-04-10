import pytest
from app.ingestion.H1_authservice import OuraAuthService
from unittest.mock import patch

client_id = "testdummy1"
secret= "testdummy2"
redirect = "testdummy3"
url = "testdummy4"
path = "some_folder/tokens.json"
scope = "testdummy6"

def test_build_url():

    authservice = OuraAuthService(client_id, secret, redirect, 
                url, path, scope)
    authurl, secure_token = authservice.build_auth_url()
    
    assert isinstance(authurl, str)
    assert client_id in authurl
    assert redirect in authurl
    assert scope in authurl

    assert isinstance(secure_token, str)
    assert len(secure_token) > 0 
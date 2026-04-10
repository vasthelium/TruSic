import pytest
from app.ingestion.H1_authservice import OuraAuthService
from unittest.mock import patch

#dummy __init__ reqs
client_id = "testdummy1"
secret= "testdummy2"
redirect = "testdummy3"
url = "testdummy4"
path = "some_folder/tokens.json"
scope = "testdummy6"

authservice = OuraAuthService(client_id, secret, redirect, 
                url, path, scope)

token_payload = {"access_token": "abc"}

@patch("authservice.json.dump")
@patch("authservice.open")
@patch("authservice.os.makedirs")
def test_savetokens(mock_makedirs, mock_open, mock_jsondump):
    authservice.save_tokens(token_payload)

    mock_makedirs.assert_called_once_with("some_folder", exist_ok=True)
    mock_open.assert_called_once_with(path, "w")
    mock_jsondump.assert_called_once_with(token_payload, mock_open.return_value.__enter__.return_value, indent=2)

# above test case can also be written without decorators
# def test_savetokens():
    
#     with patch("authservice.os.makedirs") as mock_makedirs, \
#         patch("authservice.open") as mock_open, \
#         patch("authservice.json.dump") as mock_jsondump:
        
#         authservice.save_tokens(token_payload)
        
#         mock_makedirs.assert_called_once_with("some_folder", exist_ok=True)
#         mock_open.assert_called_once_with(path, "w")
#         mock_jsondump.assert_called_once_with(token_payload, mock_open.return_value.__enter__.return_value, indent=2)
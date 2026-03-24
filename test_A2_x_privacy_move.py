import pytest
from A2_x_privacy_move import movefiles
from unittest.mock import patch

@patch("k2_privacy_move.shutil.move")
@patch("k2_privacy_move.os.path.exists")
@patch("k2_privacy_move.privacy_switch")
def test_file_movetest(mock_privacy, mock_exists, mock_move):
    mock_privacy.return_value = (
        [], 
        [{"file_name": "anything.m4a"}]
        )
    mock_exists.return_value = True

    movefiles()

    expected_source = "/Users/hussain/raw_soundfiles/anything.m4a"
    expected_destination = "/Users/hussain/raw_soundfiles_trash"

    mock_move.assert_called_once_with(expected_source, expected_destination)

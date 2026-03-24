import pytest
from A3_classify import classify
from unittest.mock import patch
import numpy as np


def test_clssify_results():

    with patch("k3_classify.privacy_switch") as mock_privacy, \
         patch("k3_classify.hub.load") as mock_load, \
         patch("k3_classify.open", create=True) as mock_open:

        mock_privacy.return_value = (
            [{
                "file_name": "anything.m4a",
                "wave_form": np.zeros(16000, dtype=np.float32),
                "sample_rate": 16000
            }],
            []
        )

        mock_open.return_value.read.return_value = (
            "0,0,Music\n"
            "1,1,Noise\n"
            "2,2,Guitar\n"
            "3,3,Piano\n"
            "4,4,Drum\n"
        )

        class FakeMap:
            def numpy(self):
                return "fake_path"

        class FakeModel:
            def __call__(self, x):
                fake_score = np.array([[0.9] + [0.0]*9])
                return fake_score, None, None

            def class_map_path(self):
                return FakeMap()

        mock_load.return_value = FakeModel()

        result = classify()

        assert mock_load.called
        assert isinstance(result, list)
        if result:
            assert isinstance(result[0], dict)

   
       
       


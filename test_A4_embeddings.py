import pytest
from app.services.A4_embeddinglayer import device, embed
import torch

def test_clap_embedding_dims():
    dev = device()
    results = embed(dev)

    assert isinstance(results, list) # assert means make sure then "isinstance" - check the type
    assert len(results) > 0 # make sure length of results is greater than zero

    first_embedding = results[0]["embedded_vector"]
    assert first_embedding.shape[-1] == 512 # make sure shape of the first_embedding is 1 dimension 512
# ==== run later =====
# def test_structure():
#     dev = device()
#     results = embed(dev)

#     assert isinstance(results, list)
#     assert len(results) > 0
#     items = results[0]
#     assert "filename" in items
#     assert "embedded_vector" in items
#     assert "sample_rate" in items


# def test_normalized():
#     dev = device()
#     results = embed(dev)

#     vec = results[0]["embedded_vector"]

#     assert isinstance(results, list)
#     assert isinstance(vec, torch.Tensor)
#     #first way
#     norm = torch.norm(vec, p=2)
#     newnorm = norm.item()
#     small_tolerance = 0.2
#     assert abs(newnorm - 1.0) < small_tolerance
#     #another way 
#     assert torch.isclose(torch.norm(vec), torch.tensor(1.0), atol=1e-5) 
#     #above line torch.isclose - elementwise approximately ewqal check
#     #somemore# 
#     #- torch.allclose(a, b, atol=...) entire tensor approximately equal - this returns True/False
#     # - comparision ops - ==, !=, <, >, <=, >=


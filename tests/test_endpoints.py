import pytest
from cl_forge.cmf import Ipc, Usd, Eur, Uf, Utm

def test_endpoint_init():
    api_key = "test_key"
    
    ipc = Ipc(api_key)
    assert ipc._client.api_key == "test_..."
    assert ipc._path == "/ipc"
    assert ipc._root_key == "IPCs"

    usd = Usd(api_key)
    assert usd._path == "/dolar"
    assert usd._root_key == "Dolares"

    eur = Eur(api_key)
    assert eur._path == "/euro"
    assert eur._root_key == "Euros"

    uf = Uf(api_key)
    assert uf._path == "/uf"
    assert uf._root_key == "UFs"

    utm = Utm(api_key)
    assert utm._path == "/utm"
    assert utm._root_key == "UTMs"

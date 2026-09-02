import pytest

from cl_forge import Ppu, calculate_verifier, exceptions, generate, validate_rut


def test_validate_rut_valid():
    assert validate_rut(12345678, "5") is True
    assert validate_rut(11222333, "9") is True
    assert validate_rut(9000000, "4") is True
    assert validate_rut(1, "9") is True

def test_validate_rut_invalid():
    assert validate_rut(12345678, "0") is False
    assert validate_rut(12345678, "K") is False

def test_calculate_verifier():
    assert calculate_verifier(12345678) == "5"
    assert calculate_verifier(11222333) == "9"
    assert calculate_verifier(9000000) == "4"
    assert calculate_verifier(1) == "9"
    assert calculate_verifier(18305086) == "9"
    assert calculate_verifier(14682029) == "8"

def test_ppu_class():
    ppu = Ppu("PHZF55")
    assert ppu.normalized == "PHZF55"
    assert ppu.verifier == "K"
    assert ppu.complete == "PHZF55-K"
    assert ppu.numeric == 69455

def test_ppu_class_3_2():
    # LLLNN -> LLL0NN
    ppu = Ppu("BBC12")
    assert ppu.normalized == "BBC012"
    assert ppu.format == "LLLNN"

def test_normalize_ppu():
    ppu = Ppu("bbc12")
    assert ppu.normalized == "BBC012"
    ppu = Ppu("bbcd12")
    assert ppu.normalized == "BBCD12"


def test_generate_success():
    n = 10
    min_val = 1_000_000
    max_val = 2_000_000
    results = generate(n, min_val, max_val)
    
    assert len(results) == n
    correlatives = set()
    for item in results:
        correlative = item['correlative']
        verifier = item['verifier']
        assert min_val <= correlative < max_val
        assert validate_rut(correlative, verifier) is True
        correlatives.add(correlative)
    
    assert len(correlatives) == n

def test_generate_seed():
    n = 5
    min_val = 1_000_000
    max_val = 2_000_000
    seed = 12345
    
    results1 = generate(n, min_val, max_val, seed=seed)
    results2 = generate(n, min_val, max_val, seed=seed)
    
    assert results1 == results2

def test_generate_invalid_input():
    # n <= 0
    with pytest.raises(exceptions.InvalidInput):
        generate(0, 1000, 2000)
    
    # min < 0
    with pytest.raises(exceptions.InvalidInput):
        generate(10, -1, 2000)
    
    # max < 0
    with pytest.raises(exceptions.InvalidInput):
        generate(10, 1000, -1)
        
    # seed < 0
    with pytest.raises(exceptions.InvalidInput):
        generate(10, 1000, 2000, seed=-5)

def test_generate_invalid_range():
    # min >= max
    with pytest.raises(exceptions.InvalidRange):
        generate(10, 2000, 1000)
    
    with pytest.raises(exceptions.InvalidRange):
        generate(10, 1000, 1000)

def test_generate_insufficient_range():
    # n > (max - min + 1)
    with pytest.raises(exceptions.InsufficientRange):
        generate(12, 1000, 1010)

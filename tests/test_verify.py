from cl_forge import verify


def test_validate_rut_valid():
    assert verify.validate_rut("12345678", "5") is True
    assert verify.validate_rut("11222333", "9") is True
    assert verify.validate_rut("9000000", "4") is True
    assert verify.validate_rut("1", "9") is True

def test_validate_rut_invalid():
    assert verify.validate_rut("12345678", "0") is False
    assert verify.validate_rut("12345678", "K") is False

def test_calculate_verifier():
    assert verify.calculate_verifier("12345678") == "5"
    assert verify.calculate_verifier("11222333") == "9"
    assert verify.calculate_verifier("9000000") == "4"
    assert verify.calculate_verifier("1") == "9"
    assert verify.calculate_verifier("18305086") == "9"
    assert verify.calculate_verifier("14682029") == "8"

def test_ppu_class():
    ppu = verify.Ppu("PHZF55")
    assert ppu.normalized == "PHZF55"
    assert ppu.verifier == "K"
    assert ppu.complete == "PHZF55-K"
    assert ppu.numeric == "069455"

def test_ppu_class_3_2():
    # LLLNN -> LLL0NN
    ppu = verify.Ppu("BBC12")
    assert ppu.normalized == "BBC012"
    assert ppu.format == "LLLNN"

def test_normalize_ppu():
    assert verify.normalize_ppu("bbc12") == "BBC012"
    assert verify.normalize_ppu("bbcd12") == "BBCD12"

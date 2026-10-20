import os
import sys

# adaug folderul radacina in path ca sa mearga importurile si cand rulez direct
RADACINA = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if RADACINA not in sys.path:
    sys.path.insert(0, RADACINA)

import pytest
from arsenal.forensics.decode import desfa, ghici_strat, citibil, decodare_straturi, sparge_xor

def test_base64():
    strat, b = desfa("U2FsdXQ=")
    assert strat == "base64"
    assert b == b"Salut"

def test_hex():
    strat, b = desfa("48656c6c6f")
    assert strat == "hex"
    assert b == b"Hello"

def test_url():
    strat, b = desfa("%2Fetc%2Fpasswd")
    assert strat == "url"
    assert b == b"/etc/passwd"

def test_ghici_strat():
    assert ghici_strat("%2Fetc") == "url"
    assert ghici_strat("48656c6c6f") == "hex"
    assert ghici_strat("U2FsdXQ=") == "base64"
    assert ghici_strat("###Invalid@@@") == "necunoscut"

def test_citibil():
    assert citibil(b"Salut, test 123!") is True
    assert citibil(b"\x00\x01\x02\xff") is False

def test_straturi_multiple():
    # exemplul din laborator: base64 -> hex -> text
    straturi, text = decodare_straturi("NTM1OTU3NTk=")
    assert "base64" in straturi
    assert "hex" in straturi
    assert text == "SYWY"

def test_xor():
    cheie = 42
    date = bytes(b ^ cheie for b in b"FLAG{test_xor_key}")
    k, clar = sparge_xor(date)
    assert k == 42
    assert clar == "FLAG{test_xor_key}"

if __name__ == "__main__":
    print("Rulare teste:")
    test_base64()
    test_hex()
    test_url()
    test_ghici_strat()
    test_citibil()
    test_straturi_multiple()
    test_xor()
    print("Toate testele au trecut!")

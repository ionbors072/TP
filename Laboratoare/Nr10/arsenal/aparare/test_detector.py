from collections import Counter
import pytest
from arsenal.aparare.detector import suspecti
from arsenal.aparare.parse_auth import esec, citeste_esecuri, pe_ip


def test_pragul_taie():
    c = Counter({"a": 13, "b": 2})
    assert suspecti(c) == [("a", 13)]
    assert suspecti(c, 2) == [("a", 13), ("b", 2)]


@pytest.mark.parametrize("prag", [0, -1])
def test_prag_invalid(prag):
    with pytest.raises(ValueError, match="prag invalid"):
        suspecti({}, prag)


def test_numarare():
    assert pe_ip([{"user": "root", "ip": "a"},
                  {"user": "ana", "ip": "a"},
                  {"user": "ana", "ip": "b"}]) == Counter(a=2, b=1)


def test_parser():
    assert esec("Failed password for root from 203.0.113.9 port 22") == ("root", "203.0.113.9")
    assert esec("Failed password for invalid user ana from ::1 port 22") == ("ana", "::1")
    assert esec("<linie stricata>") is None
    assert esec("Accepted password for root from a port 22") is None


def test_citire_robusta(tmp_path):
    cale = tmp_path / "auth.log"
    cale.write_bytes(b"stricat\xff\nFailed password for root from a port 22\n")
    assert citeste_esecuri(cale) == [{"user": "root", "ip": "a"}]


def test_fisier_lipsa(tmp_path, capsys):
    assert citeste_esecuri(tmp_path / "lipsa.log") == []
    assert "nu gasesc" in capsys.readouterr().err


def test_sortare_si_lista_goala():
    assert suspecti({"b": 2, "a": 13}, 2) == [("a", 13), ("b", 2)]
    assert suspecti({}) == []

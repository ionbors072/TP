import json
import pytest
from arsenal.windows.inventar import Proces, Eveniment, Inventar, evenimente_din_json


def test_proces_din_temp_e_suspect():
    assert Proces(1, "x.exe", "ana", r"C:\Users\ana\AppData\Local\Temp\x.exe").e_suspect() is True


def test_proces_din_windows_nu_e_suspect():
    assert Proces(2, "svchost.exe", "SYSTEM", r"C:\Windows\System32\svchost.exe").e_suspect() is False


def test_roaming_si_litere_mici():
    assert Proces(3, "x.exe", "ana", r"C:\Users\ana\appdata\roaming\x.exe").e_suspect()
    assert not Proces(4, "x.exe", "ana", r"C:\Templates\x.exe").e_suspect()


@pytest.mark.parametrize("id,nivel,rezultat", [
    (4625, "warning", True), (1102, "information", True),
    (7045, "information", True), (1, "critical", True),
    (4624, "information", False)])
def test_eveniment(id, nivel, rezultat):
    assert Eveniment(id, nivel, "Windows", "ana", "mesaj").e_suspect() is rezultat


def test_inventar_si_egalitate(tmp_path):
    cale = tmp_path / "procese.json"
    cale.write_text(json.dumps([
        {"pid": 1, "nume": "a", "user": "ana", "cale": "C:/Temp/a"},
        {"pid": 2, "nume": "b", "user": "ana", "cale": "C:/Windows/b"},
        {"pid": 3, "nume": "c", "user": "SYSTEM", "cale": "C:/Windows/c"}
    ]), encoding="utf-8")
    inv = Inventar.din_json(cale)
    assert len(inv) == 3
    assert inv.suspecte() == [Proces(1, "a", "ana", "C:/Temp/a")]
    assert inv.pe_user() == {"ana": ["a", "b"], "SYSTEM": ["c"]}
    assert Proces(1, "a", "ana", "x") == Proces(1, "a", "ana", "x")


def test_evenimente_json(tmp_path):
    cale = tmp_path / "evenimente.json"
    cale.write_text('[{"id":4625,"nivel":"warning","sursa":"Security","cont":"ana","mesaj":"esec"}]', encoding="utf-8")
    assert evenimente_din_json(cale) == [Eveniment(4625, "warning", "Security", "ana", "esec")]


def test_inventar_gol():
    inv = Inventar([])
    assert len(inv) == 0
    assert inv.suspecte() == []
    assert inv.pe_user() == {}

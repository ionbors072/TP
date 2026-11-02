from arsenal.privesc.diferenta import diferenta


def test_doar_ce_e_nou():
    acum = {"a", "b", "c"}
    baza = {"a", "b", "d"}
    assert diferenta(acum, baza) == {"c"}

import argparse
from pathlib import Path

from arsenal.privesc.enum import GTFO, citeste_linii, nume


def cai(fisier):
    return set(citeste_linii(fisier))


def diferenta(acum, baza):
    return acum - baza


def main():
    p = argparse.ArgumentParser(description="SUID noi fata de sistemul curat")
    p.add_argument("capturi")
    a = p.parse_args()
    d = Path(a.capturi)

    baza = cai(d / "baza_suid.txt")
    acum = cai(d / "suid.txt")
    print("baza:", len(baza), " acum:", len(acum))

    noi = diferenta(acum, baza)
    print(len(noi), "SUID noi fata de sistemul curat")
    for c in sorted(noi):
        print(" ", c)

    risc = {nume(c): ("mare" if nume(c) in GTFO else "normal")
            for c in sorted(noi)}
    periculoase = [c for c in sorted(noi) if risc[nume(c)] == "mare"]
    print("periculoase NOI:", periculoase)


if __name__ == "__main__":
    main()

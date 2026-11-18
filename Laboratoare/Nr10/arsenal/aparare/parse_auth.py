"""Citirea si numararea esecurilor de autentificare SSH."""
import argparse
from collections import Counter
import re
import sys

TIPAR = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\S+) port")


def esec(linie):
    m = TIPAR.search(linie)
    return (m.group(1), m.group(2)) if m else None


def citeste_esecuri(cale):
    esecuri = []
    try:
        with open(cale, encoding="utf-8", errors="replace") as f:
            for linie in f:
                r = esec(linie)
                if r is not None:
                    esecuri.append({"user": r[0], "ip": r[1]})
    except FileNotFoundError:
        print(f"nu gasesc {cale}", file=sys.stderr)
    except OSError as exc:
        print(f"nu pot citi {cale}: {exc}", file=sys.stderr)
    return esecuri


def pe_ip(esecuri):
    return Counter(e["ip"] for e in esecuri)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("log")
    a = p.parse_args()
    esecuri = citeste_esecuri(a.log)
    print(f"Esecuri de autentificare: {len(esecuri)}")
    for ip, n in pe_ip(esecuri).most_common():
        print(f"  {ip}: {n}")


if __name__ == "__main__":
    main()

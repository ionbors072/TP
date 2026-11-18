"""Detector de brute force cu prag reglabil si raport JSON."""
import argparse
import json
from arsenal.aparare.parse_auth import citeste_esecuri, pe_ip


def suspecti(counts, prag=10):
    if prag < 1:
        raise ValueError(f"prag invalid: {prag} (cel putin 1)")
    return sorted(
        [(ip, n) for ip, n in counts.items() if n >= prag],
        key=lambda pereche: pereche[1], reverse=True,
    )


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("log")
    p.add_argument("--prag", type=int, default=10)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    try:
        suspecti({}, a.prag)
    except ValueError as exc:
        p.error(str(exc))
    esecuri = citeste_esecuri(a.log)
    counts = pe_ip(esecuri)
    sus = suspecti(counts, a.prag)
    if a.json:
        print(json.dumps({"esecuri": len(esecuri), "pe_ip": dict(counts),
                          "suspecti": sus}, indent=2, ensure_ascii=False))
    else:
        print(f"Esecuri de autentificare: {len(esecuri)}")
        for ip, n in counts.most_common():
            print(f"  {ip}: {n}")
        print(f"Suspecti (prag {a.prag}):")
        for ip, n in sus:
            print(f"  {ip}  ({n} incercari)  BRUTE FORCE")


if __name__ == "__main__":
    main()

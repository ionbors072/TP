"""Inventar de procese Windows si evenimente de securitate."""
import argparse
from dataclasses import dataclass, asdict
import json
from pathlib import Path

CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")
SUSPECTE_ID = {4625, 1102, 7045}


@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str

    def e_suspect(self):
        cale = self.cale.replace("/", "\\").casefold()
        return any(fragment.casefold() in cale for fragment in CAI_SUSPECTE)


@dataclass
class Eveniment:
    id: int
    nivel: str
    sursa: str
    cont: str
    mesaj: str

    def e_suspect(self):
        return self.id in SUSPECTE_ID or self.nivel.casefold() == "critical"


def procese_din_json(cale):
    with open(cale, encoding="utf-8-sig") as f:
        return [Proces(**d) for d in json.load(f)]


def evenimente_din_json(cale):
    with open(cale, encoding="utf-8-sig") as f:
        return [Eveniment(**d) for d in json.load(f)]


@dataclass
class Inventar:
    procese: list[Proces]

    @classmethod
    def din_json(cls, cale):
        return cls(procese_din_json(cale))

    def __len__(self):
        return len(self.procese)

    def suspecte(self):
        return [p for p in self.procese if p.e_suspect()]

    def pe_user(self):
        grupuri = {}
        for p in self.procese:
            grupuri.setdefault(p.user, []).append(p.nume)
        return grupuri


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    try:
        inv = Inventar.din_json(Path(a.capturi) / "procese.json")
        ev = evenimente_din_json(Path(a.capturi) / "evenimente.json")
        suspecte = inv.suspecte()
        alarma = [e for e in ev if e.e_suspect()]
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        p.error(f"capturi invalide sau inaccesibile: {exc}")
    if a.json:
        print(json.dumps({"procese_suspecte": [asdict(x) for x in suspecte],
                          "evenimente_alarma": [asdict(x) for x in alarma]},
                         indent=2, ensure_ascii=False))
    else:
        print(f"Procese: {len(inv)} | suspecte: {len(suspecte)}")
        for proces in suspecte:
            print(f"  [{proces.pid}] {proces.nume}  ({proces.user})  {proces.cale}")
        print(f"Evenimente: {len(ev)} | alarma: {len(alarma)}")
        for e in alarma:
            print(f"  {e.id} [{e.nivel}] {e.cont}: {e.mesaj}")


if __name__ == "__main__":
    main()

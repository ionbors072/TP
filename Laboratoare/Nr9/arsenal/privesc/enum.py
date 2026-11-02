import argparse
import json
from pathlib import Path

GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash",
        "less", "awk", "python3", "perl"}


def citeste_linii(cale):
    with open(cale, encoding="utf-8") as f:
        return [linie.strip() for linie in f
                if linie.strip() and not linie.lstrip().startswith("#")]


def nume(cale):
    return cale.rsplit("/", 1)[-1]


def suid_constatari(cale):
    return [
        {"cale": c, "nume": nume(c),
         "risc": "mare" if nume(c) in GTFO else "normal"}
        for c in sorted(set(citeste_linii(cale)))
    ]


def sudo_constatari(cale):
    out = []
    for linie in citeste_linii(cale):
        user, drept = linie.split(" : ", 1)
        out.append({"user": user.strip(), "drept": drept.strip(),
                    "risc": "mare" if "NOPASSWD" in drept else "normal"})
    return out


def cron_constatari(cale):
    out = []
    for linie in citeste_linii(cale):
        campuri = linie.split()
        out.append({"user": campuri[5], "comanda": " ".join(campuri[6:])})
    return out


def enumereaza(d):
    d = Path(d)
    return {
        "suid": suid_constatari(d / "suid.txt"),
        "sudo": sudo_constatari(d / "sudo.txt"),
        "cron": cron_constatari(d / "crontab.txt"),
    }


def main():
    p = argparse.ArgumentParser(description="Analiza capturilor SUID, sudo si cron")
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    raport = enumereaza(a.capturi)
    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return

    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print(f"{categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")

    utilizatori = ({c["user"] for c in raport["sudo"]}
                   | {c["user"] for c in raport["cron"]})
    print("utilizatori implicati:", ", ".join(sorted(utilizatori)))

    destinatie = Path(__file__).with_name("enum.json")
    with open(destinatie, "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)
    print("Raport salvat in enum.json")


if __name__ == "__main__":
    main()

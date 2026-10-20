import argparse
import base64
import hashlib
import json
import os
import re
from urllib.parse import unquote

# A2. ghicim tipul de codare dupa caractere
def ghici_strat(s: str) -> str:
    s = s.strip()
    if not s:
        return "necunoscut"

    # verificam intai url (%xx)
    if re.search(r"%[0-9a-fA-F]{2}", s):
        return "url"

    # hex: doar caractere 0-9 a-f si lungime para
    if len(s) % 2 == 0 and len(s) >= 2 and re.fullmatch(r"[0-9a-fA-F]+", s):
        return "hex"

    # base64: caractere specifice si lungime multiplu de 4
    if len(s) % 4 == 0 and len(s) >= 4 and re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s):
        return "base64"

    return "necunoscut"


# A3. decodam in functie de stratul recunoscut
def desfa(s: str):
    strat = ghici_strat(s)
    try:
        if strat == "base64":
            return strat, base64.b64decode(s.strip())
        elif strat == "hex":
            return strat, bytes.fromhex(s.strip())
        elif strat == "url":
            return strat, unquote(s.strip()).encode("utf-8")
    except Exception:
        pass
    return "necunoscut", s.encode()


# A4. verificam daca toti octetii sunt caractere ascii citibile (32..126)
def citibil(b: bytes) -> bool:
    return len(b) > 0 and all(32 <= c < 127 for c in b)


# decodam in bucla pana cand dam de text clar
def decodare_straturi(val: str, max_iteratii: int = 8):
    straturi = []
    curent = val.strip()
    text_final = curent

    for _ in range(max_iteratii):
        strat, b = desfa(curent)
        if strat == "necunoscut":
            break

        if citibil(b):
            straturi.append(strat)
            try:
                curent = b.decode("utf-8")
                text_final = curent
            except UnicodeDecodeError:
                break
        else:
            # daca am ajuns la octeti necitibili ne oprim
            break

    return straturi, text_final


# A5. scor simplu pentru a gasi textul clar la XOR
def scor_text(b: bytes) -> float:
    if not citibil(b):
        return -1000.0

    text = b.lower()
    scor = 0.0

    # daca contine flag e clar ca e solutia buna
    if b"flag{" in text:
        scor += 1000.0

    # verificam procentul de vocale (in text normal e in jur de 30%)
    vocale = sum(1 for c in text if c in b"aeiou")
    if 0.20 <= (vocale / len(b)) <= 0.50:
        scor += 100.0

    # adaugam puncte pentru litere si spatii, scadem pentru caractere ciudate
    scor += sum(2.0 for c in b if c in b" _")
    scor += sum(1.0 for c in b if (65 <= c <= 90 or 97 <= c <= 122 or 48 <= c <= 57))
    scor -= sum(10.0 for c in b if c in b"~^`\\@|[]<>")

    return scor


def sparge_xor(date_sau_cale):
    if isinstance(date_sau_cale, str) and os.path.isfile(date_sau_cale):
        with open(date_sau_cale, "rb") as f:
            date = f.read()
    else:
        date = date_sau_cale

    cheie_buna = None
    text_bun = None
    scor_max = -9999.0

    # incercam toate cele 256 de chei posibile (1 octet)
    for k in range(256):
        clar = bytes(b ^ k for b in date)
        if citibil(clar):
            s = scor_text(clar)
            if s > scor_max:
                scor_max = s
                cheie_buna = k
                text_bun = clar.decode("utf-8", errors="ignore")

    return cheie_buna, text_bun


# A6. spargem hash-ul comparand cu wordlist-ul
def sparge_hash(cale_hashuri: str, cale_wordlist: str):
    with open(cale_hashuri, "r", encoding="utf-8") as f:
        tinta = f.readline().strip().lower()

    # determinam algoritmul dupa lungimea hash-ului
    if len(tinta) == 32:
        algo = "md5"
    elif len(tinta) == 40:
        algo = "sha1"
    elif len(tinta) == 64:
        algo = "sha256"
    else:
        return "necunoscut", None, tinta

    with open(cale_wordlist, "r", encoding="latin1") as f:
        for linie in f:
            cuv = linie.strip()
            if getattr(hashlib, algo)(cuv.encode("utf-8")).hexdigest() == tinta:
                return algo, cuv, tinta

    return algo, None, tinta


# A7. parsare argumente si salvare fisa.json
def main():
    parser = argparse.ArgumentParser(description="Decoder forensics")
    parser.add_argument("intrare", help="Sirul sau calea catre fisier")
    parser.add_argument("--fisier", action="store_true", help="Seteaza daca intrarea este fisier")
    parser.add_argument("--iesire-fisa", default="arsenal/forensics/fisa.json")
    parser.add_argument("--xor", help="Fisier binar xor")
    parser.add_argument("--hashuri", help="Fisier cu hashuri")
    parser.add_argument("--wordlist", default="probe/wordlist.txt")
    args = parser.parse_args()

    if args.fisier:
        with open(args.intrare, "r", encoding="utf-8") as f:
            continut = f.read().strip()
    else:
        continut = args.intrare.strip()

    straturi, rezultat = decodare_straturi(continut)
    print(f"[+] Straturi: {' -> '.join(straturi) if straturi else 'necunoscut'}")
    print(f"[+] Rezultat: {rezultat}")

    fisa = {
        "strat": straturi[-1] if straturi else "necunoscut",
        "straturi_succesive": straturi,
        "intrare": continut,
        "rezultat": rezultat
    }

    # verificam si xor daca exista fisierul
    fisier_xor = args.xor or ("probe/xor.bin" if os.path.exists("probe/xor.bin") else None)
    if fisier_xor:
        k, txt = sparge_xor(fisier_xor)
        fisa["xor"] = {"cheie": k, "clar": txt}
        print(f"[+] XOR spart: cheie {k} -> {txt}")

    # verificam si hash daca exista
    fisier_hash = args.hashuri or ("probe/hashuri.txt" if os.path.exists("probe/hashuri.txt") else None)
    if fisier_hash and os.path.exists(args.wordlist):
        algo, parola, h = sparge_hash(fisier_hash, args.wordlist)
        fisa["hash"] = {"algoritm": algo, "hash": h, "parola": parola}
        print(f"[+] Hash {algo} spart -> {parola}")

    os.makedirs(os.path.dirname(args.iesire_fisa), exist_ok=True)
    with open(args.iesire_fisa, "w", encoding="utf-8") as f:
        json.dump(fisa, f, indent=4, ensure_ascii=False)
    print(f"[+] Fisa salvata in {args.iesire_fisa}")


if __name__ == "__main__":
    main()

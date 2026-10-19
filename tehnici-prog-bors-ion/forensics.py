import os
import re
import zipfile
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# B1. verificam primii octeti (magic bytes) pentru a afla tipul real
def tip_real(cale: str) -> str:
    with open(cale, "rb") as f:
        cap = f.read(8)

    if cap.startswith(b"%PDF"):
        return "pdf"
    if cap.startswith(b"\x89PNG"):
        return "png"
    if cap.startswith(b"\xff\xd8"):
        return "jpeg"
    if cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return cap.hex()


# B2. scoatem textul imprimabil din fisier binar (asemanator cu comanda strings)
def extrage_strings(cale: str, min_len: int = 4):
    with open(cale, "rb") as f:
        date = f.read()
    # cautam secvente de caractere ascii intre spatiu (32) si tilda (126)
    rezultate = re.findall(rb"[ -~]{" + str(min_len).encode("ascii") + rb",}", date)
    return [m.decode("ascii", errors="ignore") for m in rezultate]


# B3. transformam coordonatele din grade/minute/secunde in grade zecimale
def dms_in_grade_zecimale(dms, ref: str) -> float:
    grade = float(dms[0])
    minute = float(dms[1])
    secunde = float(dms[2])
    zecimal = grade + (minute / 60.0) + (secunde / 3600.0)
    if ref in ["S", "W"]:
        zecimal = -zecimal
    return zecimal


def extrage_exif_gps(cale_foto: str):
    img = Image.open(cale_foto)
    exif = img._getexif() or {}

    gps_dict = {}
    for id_tag, val in exif.items():
        nume = TAGS.get(id_tag, id_tag)
        if nume == "GPSInfo":
            for gps_id, gps_val in val.items():
                gps_dict[GPSTAGS.get(gps_id, gps_id)] = gps_val

    if not gps_dict:
        return None, None

    lat = dms_in_grade_zecimale(gps_dict.get("GPSLatitude", (0, 0, 0)), gps_dict.get("GPSLatitudeRef", "N"))
    lon = dms_in_grade_zecimale(gps_dict.get("GPSLongitude", (0, 0, 0)), gps_dict.get("GPSLongitudeRef", "E"))
    return lat, lon


# B4. cautam semnatura de arhiva zip (PK\x03\x04) si o decupam
def carve_fisier_ascuns(cale_sursa: str, cale_iesire_zip: str = "gasit.zip"):
    with open(cale_sursa, "rb") as f:
        date = f.read()

    i = date.find(b"PK\x03\x04")
    if i != -1:
        with open(cale_iesire_zip, "wb") as f_out:
            f_out.write(date[i:])
        print(f"[+] Arhiva ZIP gasita la octetul {i} si salvata in {cale_iesire_zip}")

        # dezarhivam sa vedem ce e inauntru
        os.makedirs("gasit_dezarhivat", exist_ok=True)
        with zipfile.ZipFile(cale_iesire_zip, "r") as z:
            z.extractall("gasit_dezarhivat")
            for nume in z.namelist():
                continut = z.read(nume).decode("utf-8", errors="ignore")
                print(f"    - continut {nume}: {continut.strip()}")
        return i, cale_iesire_zip
    else:
        print("[-] Nu am gasit arhiva ZIP")
        return -1, None


# B5. ascundem un mesaj in ultimii biti ai pixelilor (LSB)
def ascunde_lsb(cale_sursa: str, mesaj: bytes, cale_iesire: str = "stego.png"):
    img = Image.open(cale_sursa).convert("RGB")
    px = list(img.getdata())

    # adaugam 0 la final ca sa stim unde se termina mesajul la citire
    mesaj_complet = mesaj + b"\x00"
    biti = "".join(f"{x:08b}" for x in mesaj_complet)

    if len(biti) > len(px) * 3:
        raise ValueError("Mesajul e prea lung pentru poza asta!")

    px_nou = []
    bit_idx = 0
    total_biti = len(biti)

    for r, g, b in px:
        canale = [r, g, b]
        for c in range(3):
            if bit_idx < total_biti:
                # modificam doar ultimul bit (& ~1 il face 0, apoi punem bitul nostru)
                canale[c] = (canale[c] & ~1) | int(biti[bit_idx])
                bit_idx += 1
        px_nou.append(tuple(canale))

    img_stego = Image.new("RGB", img.size)
    img_stego.putdata(px_nou)
    # salvam obligatoriu ca PNG (fara pierdere de informatie)
    img_stego.save(cale_iesire, "PNG")
    print(f"[+] Mesaj ascuns salvat in {cale_iesire}")


# B6. citim inapoi mesajul din pixelii pozei
def dezvaluie_lsb(cale_stego: str = "stego.png") -> str:
    img = Image.open(cale_stego).convert("RGB")
    px = list(img.getdata())

    biti = []
    for r, g, b in px:
        biti.append(str(r & 1))
        biti.append(str(g & 1))
        biti.append(str(b & 1))

    sir_biti = "".join(biti)
    octeti = bytearray()

    # grupam cate 8 biti
    for i in range(0, len(sir_biti), 8):
        chunk = sir_biti[i:i+8]
        if len(chunk) < 8:
            break
        val = int(chunk, 2)
        if val == 0:  # am dat de octetul nul de final
            break
        octeti.append(val)

    return octeti.decode("utf-8", errors="ignore")


def main():
    print("=== Lucrarea B: Forensics si Steganografie ===")

    print("\n1. Magic Bytes:")
    for fisier in ["probe/foto.jpg", "probe/ascuns.png"]:
        if os.path.exists(fisier):
            print(f"   {fisier} -> {tip_real(fisier)}")

    print("\n2. Strings in probe/ascuns.png:")
    if os.path.exists("probe/ascuns.png"):
        s = extrage_strings("probe/ascuns.png")
        print(f"   gasite {len(s)} siruri, primele cateva: {s[:5]}")

    print("\n3. Coordonate GPS din foto.jpg:")
    if os.path.exists("probe/foto.jpg"):
        lat, lon = extrage_exif_gps("probe/foto.jpg")
        if lat is not None:
            print(f"   Latitudine: {lat:.6f}")
            print(f"   Longitudine: {lon:.6f}")

    print("\n4. File carving:")
    if os.path.exists("probe/ascuns.png"):
        carve_fisier_ascuns("probe/ascuns.png")

    print("\n5. Steganografie LSB:")
    if os.path.exists("probe/foto.jpg"):
        mesaj = b"FLAG{ascuns_in_pixeli}"
        ascunde_lsb("probe/foto.jpg", mesaj, "stego.png")
        mesaj_gasit = dezvaluie_lsb("stego.png")
        print(f"   Mesaj extras din stego.png: {mesaj_gasit}")


if __name__ == "__main__":
    main()

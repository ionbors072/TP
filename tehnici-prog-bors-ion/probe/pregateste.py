import os
import io
import zipfile
import hashlib
import base64
from urllib.parse import quote
from PIL import Image, ExifTags

def pregateste_tot():
    os.makedirs("probe", exist_ok=True)

    # 1. generam mesajul codificat in mai multe straturi (text -> url -> hex -> base64)
    text_clar = "FLAG{forensics_strat_multiplu_descoperit}"
    pas1_url = quote(text_clar)
    pas2_hex = pas1_url.encode("utf-8").hex()
    pas3_b64 = base64.b64encode(pas2_hex.encode("utf-8")).decode("utf-8")
    with open("probe/mesaj.txt", "w", encoding="utf-8") as f:
        f.write(pas3_b64)

    # 2. mesaj criptat cu xor pe 1 octet (cheia este 55)
    cheie_xor = 55
    text_xor = b"FLAG{spargere_xor_simpla_si_rapida}"
    date_xor = bytes(b ^ cheie_xor for b in text_xor)
    with open("probe/xor.bin", "wb") as f:
        f.write(date_xor)

    # 3. hash md5 si dictionar pentru atacul de dictionar
    parola = "cibersecuritate2026"
    h = hashlib.md5(parola.encode("utf-8")).hexdigest()
    with open("probe/hashuri.txt", "w", encoding="utf-8") as f:
        f.write(h + "\n")

    cuvinte = ["admin", "123456", "parola", "student", "utm", "fcim", "cibersecuritate2026", "root"]
    with open("probe/wordlist.txt", "w", encoding="latin1") as f:
        f.write("\n".join(cuvinte) + "\n")

    # 4. poza cu coordonate gps in metadatele exif
    img = Image.new("RGB", (200, 200), color=(52, 152, 219))
    exif = img.getexif()
    gps_ifd = exif.get_ifd(ExifTags.IFD.GPSInfo)
    gps_ifd[1] = "N"
    gps_ifd[2] = (47.0, 1.0, 28.2)
    gps_ifd[3] = "E"
    gps_ifd[4] = (28.0, 49.0, 55.9)
    img.save("probe/foto.jpg", "JPEG", exif=exif)

    # 5. poza png cu o arhiva zip lipita la final (pentru carving)
    img_png = Image.new("RGB", (120, 120), color=(46, 204, 113))
    buf_png = io.BytesIO()
    img_png.save(buf_png, format="PNG")
    png_data = buf_png.getvalue()

    # arhiva zip cu secret.txt
    buf_zip = io.BytesIO()
    with zipfile.ZipFile(buf_zip, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("secret.txt", "FLAG{carving_reusit_arhiva_a_fost_dezarhivata}\nFisier extras din coada imaginii PNG.")
    zip_data = buf_zip.getvalue()

    with open("probe/ascuns.png", "wb") as f:
        f.write(png_data + zip_data)

    # 6. challenge optional (xor + base64)
    flag_challenge = b"FLAG{challenge_rezolvat_expert_forensics}"
    xor_chal = bytes(b ^ 0x5A for b in flag_challenge)
    b64_chal = base64.b64encode(xor_chal)
    with open("probe/challenge.bin", "wb") as f:
        f.write(b64_chal)

    print("[+] Probele de laborator au fost generate.")

if __name__ == "__main__":
    pregateste_tot()

# Raport de Laborator 6: Informații invizibile, forensics și steganografie

**Disciplina:** Tehnici de Programare  
**Instituția:** Universitatea Tehnică a Moldovei (UTM) · FCIM · Securitate Informațională  
**Student:** Borș Ion  
**Data:** 15 octombrie 2026  

---

## 1. Introducere și Obiective
Laboratorul a avut ca scop aprofundarea conceptelor de analiză a fișierelor (forensics) și ascundere a datelor (steganografie) prin dezvoltarea a două instrumente modulare în Python:
1. **Decoder universal (`arsenal/forensics/decode.py`)**: Detectează tipul de encodare (Base64, Hex, URL), decodează în cascadă straturi multiple, realizează atac de tip forță brută pe criptare XOR pe 1 octet (256 de chei) și sparge hash-uri prin dicționar de parole.
2. **Instrument de analiză fișiere și steganografie (`forensics.py`)**: Validează tipul real al fișierelor pe baza semnăturilor binare (magic bytes), extrage șiruri imprimabile (`strings`), parsează metadate EXIF și coordonate GPS, extrage arhive ascunse prin concatenare (*file carving*) și implementează steganografia LSB (*Least Significant Bit*) pentru ascunderea și recuperarea de mesaje secrete dintr-o imagine.

---

## 2. Lucrarea A: Decoderul Universal (`arsenal/forensics/decode.py`)

### A2 & A3 & A4. Recunoașterea și Desfacerea Straturilor Multiple
Pentru fișierul de test `probe/mesaj.txt`, decoderul a aplicat bucla de desfacere a straturilor în mod automat:
- **Șir inițial:** `NDY0YzQxNDcyNTM3NDI2NjZmNzI2NTZlNzM2OTYzNzM1ZjczNzQ3MjYxNzQ1ZjZkNzU2Yzc0Njk3MDZjNzU1ZjY0NjU3MzYzNmY3MDY1NzI2OTc0MjUzNzQ0`
- **Lanț de decodare identificat:**
  1. `base64` $\rightarrow$ șir hexazecimal: `464c4147253742666f72656e736963735f73747261745f6d756c7469706c755f646573636f7065726974253744`
  2. `hex` $\rightarrow$ șir URL encoded: `FLAG%7Bforensics_strat_multiplu_descoperit%7D`
  3. `url` $\rightarrow$ text clar ASCII
- **Mesaj decodificat final:**  
  ```text
  FLAG{forensics_strat_multiplu_descoperit}
  ```

### A5. Spargere Criptare XOR cu Cheie de 1 Octet (`probe/xor.bin`)
S-a parcurs spațiul de căutare de 256 de chei posibile ($k \in [0, 255]$). Printr-un sistem de evaluare a caracterelor și frecvenței textului în limbaj natural:
- **Cheie identificată:** `55` (hex: `0x37`)
- **Text clar recuperat:**  
  ```text
  FLAG{spargere_xor_simpla_si_rapida}
  ```

### A6. Spargere Hash prin Dicționar (`probe/hashuri.txt`)
- **Hash țintă:** `b41669104dd91161851fd38c38218b32`
- **Lungime:** 32 caractere hexazecimale $\rightarrow$ algoritm detectat automat: **MD5**
- **Dicționar utilizat:** `probe/wordlist.txt`
- **Parolă găsită:**  
  ```text
  cibersecuritate2026
  ```

### A7. Fișa JSON și Teste Unitare
- Rezultatele execuției au fost salvate automat în fișierul `arsenal/forensics/fisa.json`.
- Testele unitare din `teste/test_decode.py` validează decodarea pentru `base64`, `hex`, `url`, recunoașterea de tip, validarea de text citibil și funcția XOR. Toate testele au trecut cu succes sub `pytest` (7 teste trecute).

---

## 3. Lucrarea B: Forensics pe Fișiere și Steganografie (`forensics.py`)

### B1. Magic Bytes (Tip real vs. Extensie)
S-au citit primii octeți din fișiere pentru determinarea tipului real:
- `probe/foto.jpg`: începe cu `\xff\xd8` $\rightarrow$ fișier autentic **JPEG**.
- `probe/ascuns.png`: începe cu `\x89PNG` $\rightarrow$ fișier autentic **PNG**.

### B2. Extragere Șiruri Imprimabile (`strings`)
Prin căutare de tip regex `[ -~]{4,}` pe octeții din `probe/ascuns.png`, au fost identificate secțiuni standard PNG (`IHDR`, `IDAT`), urmate de șiruri suspecte la sfârșitul fișierului ce indicau prezența unui fișier adițional concatenat (`PK\x03\x04`, `secret.txt`).

### B3. Metadate EXIF și Geopoziționare (GPS)
Din imaginea `probe/foto.jpg` s-a extras tag-ul GPS `34853`. Coordonatele au fost convertite din format DMS (grade, minute, secunde) în format zecimal:
- **Latitudine:** `47.024500° N`
- **Longitudine:** `28.832194° E`
- **Locație fizică:** Chișinău, Republica Moldova (Campusul UTM Rîșcani / FCIM).
- **Legătură hartă:** [Google Maps](https://www.google.com/maps?q=47.024500,28.832194)

### B4. File Carving (Extragere Fișier Ascuns)
S-a localizat semnătura binară a unei arhive ZIP (`b"PK\x03\x04"`) la offset-ul `345` în interiorul `probe/ascuns.png`.
- Segmentul a fost decupat și salvat ca `gasit.zip`.
- La dezarhivare, fișierul conținea `secret.txt` cu mesajul:
  ```text
  FLAG{carving_reusit_arhiva_a_fost_dezarhivata}
  ```

### B5 & B6. Steganografie LSB (Least Significant Bit)
- **Ascundere:** Mesajul `FLAG{ascuns_in_pixeli}` a fost convertit în biți (cu terminator `\x00` la final) și inserat în ultimul bit al fiecărui canal de culoare RGB din `probe/foto.jpg`. Rezultatul a fost salvat ca fișier PNG fără pierderi în `stego.png`.
- **Dezvăluire:** Scriptul a citit biții LSB din `stego.png`, i-a regrupat în octeți și a oprit citirea la întâlnirea primului octet nul.
- **Mesaj reconstituit:**  
  ```text
  FLAG{ascuns_in_pixeli}
  ```

---

## 4. Provocare Opțională (Pentru Vârful Sălii)
Fișierul `probe/challenge.bin` a fost inspectat:
- Conținea un strat de encodare Base64 aplicat peste o criptare XOR pe un octet.
- După decodarea Base64 și aplicarea spargerii XOR brute-force, s-a descoperit cheia `90` (`0x5A`).
- **Flag recuperat:**  
  ```text
  FLAG{challenge_rezolvat_expert_forensics}
  ```

---

## 5. Concluzii
1. **Analiza Magic Bytes** este critică în securitate și forensics: extensia fișierului poate fi falsificată cu ușurință, dar antetul binar dezvăluie natura reală a fișierului.
2. **Eliminarea metadatelor EXIF/GPS** este esențială înainte de publicarea imaginilor în spațiul public pentru prevenirea scurgerilor de informații de geolocație (OSINT).
3. **Steganografia LSB** permite transmiterea camuflată a datelor fără modificări vizibile, însă este vulnerabilă la conversii de format cu pierdere (cum ar fi salvarea în format JPEG).

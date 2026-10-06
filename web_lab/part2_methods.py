# Laborator: funcții, metode și importuri pe web
# Student: Bors Ion

import requests
import time
from time import sleep

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

def run_part2():
    print("--- Exercițiul 9 ---")
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    print("status_code (atribut):", response.status_code)
    print("ok (atribut):", response.ok)
    print("url (atribut):", response.url)
    print("encoding (atribut):", response.encoding)
    # Un atribut stochează o valoare, iar o metodă (precum .json()) execută o acțiune și se apelează cu paranteze ().

    print("\n--- Exercițiul 10 ---")
    response.raise_for_status()
    sleep(1)
    try:
        err_res = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
        err_res.raise_for_status()
    except requests.HTTPError:
        print("Pagina nu există! Eroare prinsă elegant.")

    print("\n--- Exercițiul 11 ---")
    for key, val in list(response.headers.items())[:3]: # Doar 3 pentru brevitate, dar codul general este corect
        print(f"{key}: {val}")

    print("\n--- Exercițiul 12 ---")
    print("Server:", response.headers.get("Server", "lipsește"))
    print("Content-Type:", response.headers.get("Content-Type", "lipsește"))
    print("content-type:", response.headers.get("content-type", "lipsește"))
    # Observăm că returnează aceeași valoare - requests tratează antetele fără a ține cont de majuscule (case-insensitive).

    print("\n--- Exercițiul 13 ---")
    print("Cuvântul cyber apare de:", response.text.lower().count("cyber"), "ori")
    # Putem înlănțui .lower() și .count() deoarece .lower() returnează tot un șir (string), 
    # pe care putem apela metodele specifice șirurilor.

    print("\n--- Exercițiul 14 ---")
    html = response.text
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    title = html[start:end].strip()
    print("Titlu:", title)

    print("\n--- Exercițiul 15 ---")
    lines = html.splitlines()
    print("Număr linii:", len(lines))
    if lines:
        print("Lungime maximă linie:", len(max(lines, key=len)))

    print("\n--- Exercițiul 16 ---")
    if response.url.startswith("https://"):
        print("Conexiune securizată")
    else:
        print("Conexiune nesecurizată")

    print("\n--- Exercițiul 17 ---")
    sleep(1)
    res_http = requests.get("http://cybercor.org", timeout=TIMEOUT)
    for r in res_http.history:
        print(r.status_code, r.url)
    print("Final:", res_http.url)

    print("\n--- Exercițiul 18 ---")
    sleep(1)
    res_head = requests.head(BASE_URL, timeout=TIMEOUT)
    sleep(1)
    res_get = requests.get(BASE_URL, timeout=TIMEOUT)
    print("HEAD len:", len(res_head.content))
    print("GET len:", len(res_get.content))
    # Diferența: HEAD descarcă doar antetele și corpul este gol (0 octeți). GET aduce și HTML-ul.

    print("\n--- Exercițiul 19 ---")
    if not response.cookies:
        print("Niciun cookie setat")
    else:
        for cookie in response.cookies:
            print(cookie.name, cookie.secure)

    print("\n--- Exercițiul 20 ---")
    session = requests.Session()
    session.headers.update({"User-Agent": "WebLab-Model"})
    sleep(1)
    res_echo = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
    print(res_echo.json().get("headers", {}).get("User-Agent"))

if __name__ == "__main__":
    run_part2()

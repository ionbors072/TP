# Laborator: funcții, metode și importuri pe web
# Student: Bors Ion

import requests
import time
from time import sleep

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

def fetch(url, timeout=10):
    return requests.get(url, timeout=timeout)

def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    response = fetch(url)
    return response.status_code

def get_title(html: str) -> str:
    """Extrage și returnează titlul din codul HTML."""
    start = html.find("<title>")
    if start == -1:
        return ""
    start += len("<title>")
    end = html.find("</title>", start)
    return html[start:end].strip() if end != -1 else ""

def page_exists(url: str) -> bool:
    """Returnează True dacă pagina se poate descărca cu succes, False altfel."""
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False

def check_paths(base: str, paths: list) -> dict:
    """Verifică o listă de căi pe un domeniu și returnează starea fiecăreia."""
    results = {}
    for path in paths:
        url = base.rstrip("/") + path
        time.sleep(1)
        results[path] = get_status(url)
    return results

def get_header(url: str, name: str, default: str = "lipsește") -> str:
    """Returnează valoarea unui anumit antet HTTP."""
    sleep(1)
    response = requests.head(url, timeout=TIMEOUT)
    return response.headers.get(name, default)

def security_headers(url: str) -> dict:
    """Verifică prezența a 5 antete de securitate HTTP."""
    headers_to_check = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]
    sleep(1)
    response = requests.head(url, timeout=TIMEOUT)
    return {h: (h in response.headers) for h in headers_to_check}

def score_headers(results: dict) -> str:
    """Returnează un scor sub forma 'X/Y' pe baza dicționarului de prezență."""
    score = sum(results.values())
    return f"{score}/{len(results)}"

def fetch_robots(base: str):
    """Returnează conținutul fișierului robots.txt sau None dacă lipsește."""
    url = base.rstrip("/") + "/robots.txt"
    try:
        sleep(1)
        res = requests.get(url, timeout=TIMEOUT)
        if res.status_code == 200:
            return res.text
    except requests.RequestException:
        pass
    return None

def disallowed_paths(robots_text) -> list:
    """Returnează o listă cu toate valorile Disallow din robots.txt."""
    if not robots_text:
        return []
    paths = []
    for line in robots_text.splitlines():
        if line.lower().startswith("disallow:"):
            parts = line.split(":", 1)
            if len(parts) > 1:
                paths.append(parts[1].strip())
    return paths

def response_times(*urls) -> dict:
    """Măsoară timpul de răspuns pentru un număr variabil de URL-uri."""
    times = {}
    for url in urls:
        time.sleep(1)
        start = time.perf_counter()
        requests.head(url, timeout=TIMEOUT)
        end = time.perf_counter()
        times[url] = end - start
    return times

def log(message, **details):
    """Afișează un mesaj însoțit de detalii."""
    details_str = " | ".join(f"{k}={v}" for k, v in details.items())
    if details_str:
        print(f"{message} | {details_str}")
    else:
        print(message)

def run_part3():
    print("--- Exercițiul 21 ---")
    sleep(1)
    res = fetch(BASE_URL)
    print("Stare fetch:", res.status_code)

    print("\n--- Exercițiul 22 ---")
    for p in ["/", "/robots.txt", "/sitemap.xml"]:
        print(f"Stare {p}:", get_status(BASE_URL + p))

    print("\n--- Exercițiul 23 ---")
    sleep(1)
    print("Fetch implicit:", fetch(BASE_URL).status_code)
    sleep(1)
    print("Fetch timeout=3:", fetch(BASE_URL, timeout=3).status_code)

    print("\n--- Exercițiul 24 ---")
    print("Titlu:", get_title(res.text))

    print("\n--- Exercițiul 25 ---")
    help(get_title)

    print("\n--- Exercițiul 26 ---")
    # Adnotările de tip (type hints) nu opresc execuția programului, ele sunt doar sugestii pentru developer / IDE.
    try:
        sleep(1)
        get_status(123)
    except Exception as e:
        print("Eroare așteptată când type hint-ul e ignorat:", type(e).__name__)

    print("\n--- Exercițiul 27 ---")
    print("Există (invalid):", page_exists("https://this-domain-does-not-exist.invalid"))

    print("\n--- Exercițiul 28 ---")
    print(check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"]))

    print("\n--- Exercițiul 29 ---")
    print("Server:", get_header(BASE_URL, name="Server"))

    print("\n--- Exercițiul 30 și 31 ---")
    sec_headers = security_headers(BASE_URL)
    print("Headers:", sec_headers)
    print("Scor:", score_headers(sec_headers))

    print("\n--- Exercițiul 32 ---")
    rtxt = fetch_robots(BASE_URL)
    print("Căi interzise:", disallowed_paths(rtxt))

    print("\n--- Exercițiul 33 ---")
    print("Timpi de răspuns:", response_times(BASE_URL, ECHO_URL))

    print("\n--- Exercițiul 34 ---")
    log("verificat", url=BASE_URL, status=200)
    # 'print' doar scrie text în consolă, în timp ce 'return' trimite valoarea înapoi în codul apelant, 
    # pentru a putea fi utilizată sau procesată mai departe.

if __name__ == "__main__":
    run_part3()

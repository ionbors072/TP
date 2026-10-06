# Laborator: funcții, metode și importuri pe web
# Student: Bors Ion

import time
import requests
import urllib.request
from requests import get
import requests as rq
from time import sleep 

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

def run_part1():
    print("--- Exercițiul 1 ---")
    print("Requests version:", requests.__version__)
    # requests a avut nevoie de pip install pentru că este o bibliotecă externă.
    # urllib nu a avut nevoie de pip install deoarece este în biblioteca standard din Python.

    print("\n--- Exercițiul 2 ---")
    sleep(1)
    response1 = requests.get(BASE_URL, timeout=TIMEOUT)
    print(response1.status_code)

    sleep(1)
    response2 = get(BASE_URL, timeout=TIMEOUT)
    print(response2.status_code)
    # 'import requests' - Avantaj: este evident de unde vine .get().
    # 'from requests import get' - Avantaj: cod mai scurt.

    print("\n--- Exercițiul 3 ---")
    sleep(1)
    response3 = rq.get(BASE_URL, timeout=TIMEOUT)
    print(response3.status_code)
    # Un alias e bun când numele e prea lung și există convenții (ex: pd, np). E rău dacă alegem nume ciudate care ascund proveniența.

    print("\n--- Exercițiul 4 ---")
    sleep(1)
    # Site-ul cybercor.org blochează agentul prestabilit "Python-urllib" cu eroarea 403 Forbidden.
    # Soluția este să "păcălim" site-ul, setând un User-Agent de browser real printr-un obiect Request.
    req = urllib.request.Request(BASE_URL, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    response4 = urllib.request.urlopen(req, timeout=TIMEOUT)
    print(response4.status)
    body = response4.read().decode("utf-8")
    print(body[:200])

    print("\n--- Exercițiul 5 ---")
    print(dir(requests))
    # get -> funcție
    # Session -> clasă
    # exceptions -> modul

    print("\n--- Exercițiul 6 ---")
    help(requests.get)
    # parametrul este timeout
    sleep(1)
    requests.get(BASE_URL, timeout=3)

    print("\n--- Exercițiul 7 ---")
    sleep(1)
    start = time.perf_counter()
    res = requests.get(BASE_URL, timeout=TIMEOUT)
    end = time.perf_counter()
    print("Timp perf_counter:", end - start)
    print("Timp response.elapsed:", res.elapsed.total_seconds())

    print("\n--- Exercițiul 8 ---")
    try:
        import bs4
        print("Modulul este instalat cu succes!")
    except ImportError:
        print("Instalați modulul cu: pip install beautifulsoup4.")

if __name__ == "__main__":
    run_part1()

# Laborator: funcții, metode și importuri pe web
# Student: Bors Ion

import requests
import time
from time import sleep
import urllib.parse
import re
from html.parser import HTMLParser
import hashlib
import json
import socket
import ssl
import datetime

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

def ex35_urlparse():
    url = "https://cybercor.org/path?x=1#top"
    parsed = urllib.parse.urlparse(url)
    print("scheme:", parsed.scheme)
    print("netloc:", parsed.netloc)
    print("path:", parsed.path)
    print("query:", parsed.query)
    print("fragment:", parsed.fragment)

def ex36_urljoin():
    print(urllib.parse.urljoin(BASE_URL, "/about"))
    print(urllib.parse.urljoin(BASE_URL, "contact.html"))
    print(urllib.parse.urljoin(BASE_URL, "../index.html"))

def extract_links(html: str) -> list:
    """Extrage toate legăturile (href) din codul HTML."""
    links = re.findall(r'href="([^"]+)"', html)
    return list(dict.fromkeys(links))

def split_links(links: list, domain: str) -> tuple:
    """Împarte legăturile în interne și externe față de domeniul dat."""
    internal = []
    external = []
    for link in links:
        full_url = urllib.parse.urljoin(f"https://{domain}", link)
        if urllib.parse.urlparse(full_url).netloc == domain:
            internal.append(full_url)
        else:
            external.append(full_url)
    return internal, external

class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)

def page_fingerprint(url: str) -> str:
    """Returnează amprenta SHA256 a conținutului paginii."""
    sleep(1)
    response = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(response.content).hexdigest()
    # Ar fi diferite doar dacă serverul returnează conținut diferit (dinamic/modificat) între cereri.

def save_and_load_headers(url: str):
    sleep(1)
    response = requests.get(url, timeout=TIMEOUT)
    with open("headers.json", "w") as file:
        json.dump(dict(response.headers), file, indent=2)
    
    with open("headers.json", "r") as file:
        loaded = json.load(file)
        print("Un antet încărcat din JSON (Server):", loaded.get("Server", "lipsește"))

def resolve(hostname: str) -> str:
    """Returnează adresa IP a domeniului."""
    return socket.gethostbyname(hostname)

def cert_days_left(hostname: str) -> int:
    """Returnează câte zile au mai rămas până la expirarea certificatului SSL."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            not_after = cert["notAfter"]
            expire_date = datetime.datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
            return (expire_date - datetime.datetime.utcnow()).days

def run_part4():
    print("--- Exercițiul 35 ---")
    ex35_urlparse()

    print("\n--- Exercițiul 36 ---")
    ex36_urljoin()

    print("\n--- Exercițiul 37 și 38 ---")
    sleep(1)
    html = requests.get(BASE_URL, timeout=TIMEOUT).text
    all_links = extract_links(html)
    domain = urllib.parse.urlparse(BASE_URL).netloc
    internal, external = split_links(all_links, domain)
    print(f"Total legături unice găsite: {len(all_links)}")
    print(f"Interne: {len(internal)}, Externe: {len(external)}")

    print("\n--- Exercițiul 39 ---")
    test_html = """
    <html><body>
      <img src="/logo.png" alt="Logo">
      <IMG SRC="poza.jpg">
      <img alt="imagine fără src">
      <img src="https://cdn.example.com/banner.webp" />
      <a href="/despre">Aceasta nu este o imagine</a>
    </body></html>
    """
    finder = ImageFinder()
    finder.feed(test_html)
    assert finder.images == [
        "/logo.png",
        "poza.jpg",
        "https://cdn.example.com/banner.webp",
    ], "Parserul nu a găsit exact imaginile așteptate"
    print("Testul pentru parser a trecut!")
    
    finder_real = ImageFinder()
    finder_real.feed(html)
    print(f"Găsite pe site real: {len(finder_real.images)} imagini.")

    print("\n--- Exercițiul 40 ---")
    print("Amprenta 1:", page_fingerprint(BASE_URL))
    print("Amprenta 2:", page_fingerprint(BASE_URL))

    print("\n--- Exercițiul 41 ---")
    save_and_load_headers(BASE_URL)

    print("\n--- Exercițiul 42 ---")
    print("IP cybercor.org:", resolve("cybercor.org"))

    print("\n--- Exercițiul 43 ---")
    print(f"Zile rămase certificat: {cert_days_left('cybercor.org')}")
    
    # Exercițiul 39 bonus question
    # Răspuns: handle_starttag() este apelată de clasa de bază HTMLParser (codul din biblioteca standard) 
    # în timp ce analizează șirul HTML pe care i l-am pasat cu metoda feed().

if __name__ == "__main__":
    run_part4()

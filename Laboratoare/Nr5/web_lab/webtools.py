# Laborator: funcții, metode și importuri pe web
# Student: Bors Ion

import requests
import time
from time import sleep
import socket
import ssl
import datetime
import urllib.parse
from bs4 import BeautifulSoup
import json

TIMEOUT = 10
DEFAULT_HEADERS = {"User-Agent": "WebLab-Model"}

def fetch(url, timeout=TIMEOUT):
    return requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)

def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    response = fetch(url)
    return response.status_code

def get_title(html: str) -> str:
    """Extrage și returnează titlul din codul HTML folosind BeautifulSoup (Bonus)."""
    soup = BeautifulSoup(html, 'html.parser')
    return soup.title.string.strip() if soup.title and soup.title.string else ""
    # Cu bs4 este mult mai simplu, scurt și sigur decât căutarea manuală de indexuri.

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
    response = requests.head(url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)
    return {h: (h in response.headers) for h in headers_to_check}

def score_headers(results: dict) -> str:
    return f"{sum(results.values())}/{len(results)}"

def resolve(hostname: str) -> str:
    return socket.gethostbyname(hostname)

def cert_days_left(hostname: str) -> int:
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            not_after = cert["notAfter"]
            expire_date = datetime.datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
            return (expire_date - datetime.datetime.utcnow()).days

def extract_links(html: str) -> list:
    """Extrage legăturile folosind BeautifulSoup (Bonus)."""
    soup = BeautifulSoup(html, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    return list(dict.fromkeys(links))
    # E mai sigur pentru că nu folosește RegEx fragil, ci un parser HTML real.

def split_links(links: list, domain: str) -> tuple:
    internal, external = [], []
    for link in links:
        full_url = urllib.parse.urljoin(f"https://{domain}", link)
        if urllib.parse.urlparse(full_url).netloc == domain:
            internal.append(full_url)
        else:
            external.append(full_url)
    return internal, external

def disallowed_paths(base_url) -> list:
    url = base_url.rstrip("/") + "/robots.txt"
    try:
        sleep(1)
        res = fetch(url)
        if res.status_code == 200:
            paths = []
            for line in res.text.splitlines():
                if line.lower().startswith("disallow:"):
                    parts = line.split(":", 1)
                    if len(parts) > 1:
                        paths.append(parts[1].strip())
            return paths
    except requests.RequestException:
        pass
    return []

def check_paths(base: str, paths: list) -> dict:
    results = {}
    for path in paths:
        url = base.rstrip("/") + path
        sleep(1)
        results[path] = get_status(url)
    return results

def site_report(url: str):
    print(f"=== Raport site: {url} ===")
    
    parsed_url = urllib.parse.urlparse(url)
    domain = parsed_url.netloc
    
    sleep(1)
    http_url = f"http://{domain}"
    try:
        res_http = requests.get(http_url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)
        redirects = []
        for r in res_http.history:
            redirects.append(f"{r.status_code} -> {r.url}")
        # redirects.append(f"Final: {res_http.url}")
        redirects_str = ", ".join(redirects) if redirects else "Niciuna"
    except requests.RequestException:
        redirects_str = "Eroare la obținerea redirecționărilor"
    
    sleep(1)
    response = fetch(url)
    status_code = response.status_code
    
    print(f"Cod de stare:      {status_code}")
    
    title = get_title(response.text)
    print(f"Titlu:             {title}")
    
    ip = resolve(domain)
    print(f"Adresă IP:         {ip}")
    
    print(f"Redirecționări:    {redirects_str}")
    
    sec_headers = security_headers(url)
    score = score_headers(sec_headers)
    print(f"Scor securitate:   {score}")
    
    days = 0
    try:
        days = cert_days_left(domain)
        cert_str = f"{days} de zile rămase"
    except Exception:
        cert_str = "Eroare certificat"
    print(f"Certificat:        {cert_str}")
    
    all_links = extract_links(response.text)
    internal, external = split_links(all_links, domain)
    print(f"Legături:          {len(internal)} interne, {len(external)} externe")
    
    forbidden = disallowed_paths(url)
    forbidden_str = ", ".join(forbidden) if forbidden else "Niciuna"
    print(f"Căi interzise:     {forbidden_str}")
    
    print("Salvat în report.json")
    
    report_data = {
        "url": url,
        "status_code": status_code,
        "title": title,
        "ip": ip,
        "redirects": redirects_str,
        "security_score": score,
        "cert_days_left": days,
        "internal_links": len(internal),
        "external_links": len(external),
        "disallowed_paths": forbidden
    }
    
    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))

import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    curat_host = host.strip().rstrip("/")
    curat_path = path.strip().lstrip("/")
    return f"https://{curat_host}/{curat_path}"


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.lower().startswith("https://")


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    try:
        response = requests.get(url, timeout=5)
        print(f"URL: {url}")
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
    except requests.RequestException as e:
        print(f"URL: {url}")
    


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        reponse = requests.get(url, timeout=5)
        raw_ct = reponse.headers.get("Content-Type", "N/A")
        if raw_ct and ";" in raw_ct:
            content_type = raw_ct.split(";")[0].strip()
        else:
            content_type = raw_ct
        server = reponse.headers.get("Server", "N/A")
        if not server:
            server = "unknown"
        length = len(reponse.content)
        return {
            "status": reponse.status_code,
            "content_type": content_type,
            "length": length,
            "server": server,
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "content_type": "N/A",
            "length": 0,
            "server": "N/A",
        }
def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    rezultate = []
    for site in SITES:
        rezultat = check_site(site)
        rezultate.append((site, rezultat))

        successful = [item for item in rezultate if item[1].get("status") == 200]

        successful.sort(key=lambda item: item[1].get("length", 0), reverse=True)

        for url, data in successful:
                print(f"{url} -> {data['status']}, {data['length']} octeți")
        reusite = len(successful)
        esuate = len(rezultate) - reusite
        print(f"Reușite: {reusite} | Eșuate: {esuate}")

def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    pass


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    pass

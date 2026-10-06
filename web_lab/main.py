# Laborator: funcții, metode și importuri pe web
# Student: Bors Ion

import argparse
import csv
from datetime import datetime
import webtools

# Exercițiul 45: Importarea anumitor nume
from webtools import get_title, security_headers
# Dacă main.py ar avea și o funcție proprie numită get_title, importul de mai sus
# ar fi suprascris (sau invers, dacă funcția e definită după import), ducând la confuzie 
# sau erori deoarece Python păstrează ultima definiție asociată numelui "get_title".

def main():
    parser = argparse.ArgumentParser(description="Analizează un site web.")
    parser.add_argument("url", help="URL-ul site-ului de analizat (ex: https://cybercor.org)")
    args = parser.parse_args()
    
    url = args.url

    print("=== Start Exercițiul 49: Raport CSV ===")
    paths_to_check = ["/", "/robots.txt", "/sitemap.xml", "/admin"]
    results = webtools.check_paths(url, paths_to_check)
    
    with open("report.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["path", "status", "checked_at"])
        now = datetime.now().isoformat()
        for p, status in results.items():
            writer.writerow([p, status, now])
    print("Salvat în report.csv.\n")
    
    print("=== Start Exercițiul 50: Raport complet site ===")
    webtools.site_report(url)

if __name__ == "__main__":
    # La rularea python main.py, `__name__` este "__main__".
    # În webtools.py, am adăugat un autotest sub `if __name__ == "__main__":`.
    # Acel autotest rulează doar când dăm direct `python webtools.py` 
    # și nu rulează aici, la `import webtools`, deoarece atunci când un modul este importat,
    # numele lui intern (`__name__`) devine "webtools", nu "__main__".
    main()

# Laboratorul 10

Rezolvare pentru lucrarile A si B. Necesita Python 3.10+; pytest este necesar doar pentru teste.

Datele din start/auth.log provin din fisierul original auth.log furnizat pentru laboratorul 10. Regulile de alarma sunt euristici de laborator, nu confirmari ale unui atac.

Deschide terminalul in acest folder (lab 10) si ruleaza:

```powershell
python -m pip install -r requirements-dev.txt
python -m arsenal.aparare.parse_auth arsenal/aparare/start/auth.log
python -m arsenal.aparare.detector arsenal/aparare/start/auth.log
python -m arsenal.aparare.detector arsenal/aparare/start/auth.log --prag 2
python -m arsenal.aparare.detector arsenal/aparare/start/auth.log --json
python -m pytest -q arsenal/aparare/test_detector.py
```

Rezultat pe datele originale: 15 esecuri, 13 pentru 203.0.113.9 si 2 pentru 198.51.100.7. Pragul implicit 10 selecteaza prima adresa. esec intoarce None pentru randuri nerecunoscute; citeste_esecuri intoarce o lista; pe_ip intoarce Counter. Un fisier lipsa produce un mesaj pe stderr si o lista goala, conform scheletului din fisa. Pragul sub 1 ridica ValueError; CLI il prezinta fara traceback. In JSON, esecuri este numarul total, pe_ip este dictionarul numaratorilor, suspecti este lista perechilor [ip, numar].

Testele folosesc date independente de capturile de start. Cele doua laboratoare se ruleaza separat deoarece fiecare are propriul pachet arsenal. Exercitiile optionale care cer o masina reala nu au fost executate. Predarea prin git ramane o etapa separata; aceste fisiere sunt pregatite local.

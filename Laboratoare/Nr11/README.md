# Laboratorul 11

Rezolvare pentru lucrarile A si B. Necesita Python 3.10+; pytest este necesar doar pentru teste.

Datele din start/procese.json si start/evenimente.json sunt extrase din arhiva originala start.zip furnizata pentru laboratorul 11. Regulile de alarma sunt euristici de laborator, nu confirmari ale unui atac.

Deschide terminalul in acest folder (lab 11) si ruleaza:

```powershell
python -m pip install -r requirements-dev.txt
python -m arsenal.windows.inventar arsenal/windows/start
python -m arsenal.windows.inventar arsenal/windows/start --json
python -m pytest -q arsenal/windows/test_inventar.py
```

Rezultat pe datele originale: 7 procese, 2 suspecte; 8 evenimente, 5 alarme. self este instanta curenta, iar cls din din_json este clasa folosita pentru constructie. Dataclass genereaza constructorul, reprezentarea si egalitatea dupa campuri. Inventar.pe_user intoarce nume grupate pe utilizator. JSON contine procese_suspecte si evenimente_alarma, serializate cu asdict. Caile Windows sunt comparate fara distinctie intre majuscule si minuscule.

Testele folosesc date independente de capturile de start. Cele doua laboratoare se ruleaza separat deoarece fiecare are propriul pachet arsenal. Exercitiile optionale care cer o masina reala nu au fost executate. Predarea prin git ramane o etapa separata; aceste fisiere sunt pregatite local.


## 🧭 2. `maybe_subtest` — Čisté testy bez podmínek

Při psaní testů, které podporují zapínání a vypínání detailních výpisů (`verbose`), vývojáři často sklouzávají k ošklivému větvení kódu:

```python
# 🛑 ŠPATNĚ: Kód plný duplicit a podmínek
if verbose:
    with subtests.test("kontrola_labelu"):
        assert exc.label == "MY_LABEL"
else:
    assert exc.label == "MY_LABEL"
```

Tento přístup brutálně nafukuje testovací soubory a zhoršuje jejich čitelnost. Nástroj `maybe_subtest` implementuje návrhový vzor **Null Object** a toto větvení kompletně schovává do jednoho elegantního context manageru.

### 📄 Kompletní kód funkce (Elegantní minimalismus):

Díky dekorátoru `@contextmanager` a generátoru je celá logika neuvěřitelně krátká a bezpečná proti únikům kontextu:

```python
from contextlib import contextmanager
from typing import Any, Iterator

@contextmanager
def maybe_subtest(
    subtests: Any,
    *,
    name: str,
    verbose: bool,
) -> Iterator[Any]:
    """Podmíněně alokuje izolovaný subtest v pytestu podle příznaku verbose."""
    if verbose:
        # Režim 1: Vytvoří se izolovaný subtest pod pytestem
        with subtests.test(name) as ctx:
            yield ctx
    else:
        # Režim 2: Žádná režie, kód se pouze propustí dál
        yield None
```

---

## 🔍 Použití ve vlastních testovacích metodách

Tento pomocník je zcela univerzální. Můžete jej velmi snadno integrovat do svých vlastních testovacích tříd, metod nebo pomocných auditorů, které potřebují dynamicky přepínat upovídanost (`verbose`) výstupu.

### Příklad integrace:

Představme si, že píšete vlastní testovací metodu pro ověření API endpointu:

```python
def assert_api_response(subtests, response, *, verbose: bool = True):
    """Vlastní auditor pro kontrolu API odpovědi."""
    
    # Krok 1: Kontrola status kódu
    with maybe_subtest(subtests, name="status_code", verbose=verbose):
        assert response.status_code == 200

    # Krok 2: Kontrola hlaviček
    with maybe_subtest(subtests, name="headers", verbose=verbose):
        assert "Content-Type" in response.headers
        assert response.headers["Content-Type"] == "application/json"

    # Krok 3: Kontrola těla odpovědi
    with maybe_subtest(subtests, name="payload_structure", verbose=verbose):
        assert "status" in response.json()
        assert response.json()["status"] == "success"
```

### Jak vypadá výstup v pytestu:

* **Při `verbose=True`:**
Pytest rozpadne každou aserci do vlastního "zeleného" bodu. Pokud krok s kontrolou hlaviček selže, test pokračuje dál a zkontroluje i tělo odpovědi.
```text
test_api.py::test_my_endpoint SUBPASSED [status_code]
test_api.py::test_my_endpoint SUBPASSED [headers]
test_api.py::test_my_endpoint SUBPASSED [payload_structure]
```


* **Při `verbose=False`:**
Všechny kroky proběhnou přímo na hlavní lince. Test běží maximální možnou rychlostí (vhodné pro CI pipeline). Jakákoli chyba test okamžitě zastaví.
```text
test_api.py::test_my_endpoint PASSED
```


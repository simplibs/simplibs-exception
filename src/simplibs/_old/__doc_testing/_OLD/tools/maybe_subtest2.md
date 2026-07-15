# 📦 Nástroj 2: `maybe_subtest` (Podmíněný context manager)

## Uživatelský průvodce: `maybe_subtest`

Při psaní robustních testovacích nástrojů chceme často podporovat dva režimy běhu testů:

* **Verbose režim (`verbose=True`):** Každý krok a každá aserce se spustí v izolovaném subtestu (`pytest-subtests`). Pokud jeden krok selže, test pokračuje a zkontroluje i ty další.
* **Tichý režim (`verbose=False`):** Test běží přímo na hlavní lince bez subtestů. Je maximálně rychlý (vhodný pro CI pipelines) a při první chybě okamžitě končí.

Standardně to vede k ošklivému větvení kódu pomocí podmínek `if verbose: with subtests.test(...):`. Nástroj `maybe_subtest` toto větvení kompletně odstraňuje a schovává pod kapotu elegantního context manageru.

---

### 📄 Kompletní kód funkce

Díky síle standardní knihovny Pythonu a `@contextmanager` je celá implementace neuvěřitelně čistá a elegantní:

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
    """Podmíněně alokuje izolovaný subtest v pytestu podle příznaku verbose.
    
    Implementuje vzor Null-Object pro context managery. V tichém režimu (verbose=False)
    pouze propustí kód dál s nulovou režií, ve verbose režimu bezpečně izoluje běh.
    """
    if verbose:
        # Režim 1: Vytvoří se izolované trasovací rozhraní pytestu
        with subtests.test(name) as ctx:
            yield ctx
    else:
        # Režim 2: Rychlý přímý průchod bez alokace subtestu
        yield None
```

---

### 🔍 Praktický příklad použití

Tento context manager je naprosto univerzální. Můžete ho skvěle využít ve svých vlastních asertivních metodách a auditorech:

```python
from simplibs.exception.testing.tools import maybe_subtest

def verify_user_profile(subtests, user, *, verbose: bool = True):
    """Vlastní komplexní kontrola uživatelského profilu."""
    
    # Krok 1: Kontrola e-mailu
    with maybe_subtest(subtests, name="check_email_format", verbose=verbose):
        assert "@" in user.email
        assert user.email.endswith(".cz")

    # Krok 2: Kontrola věku
    with maybe_subtest(subtests, name="check_age_limit", verbose=verbose):
        assert user.age >= 18

    # Krok 3: Kontrola oprávnění
    with maybe_subtest(subtests, name="check_active_status", verbose=verbose):
        assert user.is_active is True
```

### 📊 Porovnání výstupů v konzoli

* **Při `verbose=True` (Detailní trasování):**
Pytest rozpadne každou aserci do vlastního sub-bloku. Pokud kontrola věku selže, test přesto pokračuje a ověří i aktivní status.
```text
test_users.py::test_user_registration SUBPASSED [check_email_format]
test_users.py::test_user_registration SUBPASSED [check_age_limit]
test_users.py::test_user_registration SUBPASSED [check_active_status]
```


* **Při `verbose=False` (Rychlá CI pipeline):**
Všechny kroky se vyhodnotí přímo na hlavní lince bez jakékoli alokační režie subtestů. Jakékoli selhání okamžitě zastaví celý test.
```text
test_users.py::test_user_registration PASSED
```



---

### 🛡️ Architektonické principy `maybe_subtest`

* **Zero Syntax Pollution (Čistý kód):** Odstraňuje duplicitní větvení a vnořené bloky `if/else` z testovacích souborů.
* **Vzor Null-Object (Bi-modal Routing):** Chová se jako inteligentní výhybka. Buď aktivuje těžký sledovací aparát Pytestu, nebo se promění v "neviditelný" průchod (yield `None`) s nulovou režií na výkon.
* **Bezpečné uvolnění zdrojů (Resource Safety):** Využití generátoru s context managerem garantuje, že kontexty subtestů se vždy bezpečně uzavřou a neuvolní žádné trasovací úniky (trace leaks) ani v případě nečekané systémové chyby.

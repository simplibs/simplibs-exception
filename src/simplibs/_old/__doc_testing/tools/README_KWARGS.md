# 📦 `Kwargs` 
**Sémantický wrapper parametrů**

## 🧩 Smysl nástroje

Při automatizovaném testování funkcí (například v maticových testech `bulk_test`) narážíme v Pythonu na zásadní typovou nejednoznačnost. Slovník `{...}` může reprezentovat:

1. **Jednu hodnotu** (např. předáváte slovník jako jeden poziční parametr `value`).
2. **Sadu pojmenovaných parametrů** (které se mají do funkce rozbalit jako `kwargs`).

Třída `Kwargs` funguje jako **sémantický štítek (token)**. Jakmile slovník zabalíte do `Kwargs`, testovací pipeline okamžitě a bezpečně ví, že jej má při volání funkce rozbalit jako pojmenované argumenty (`kwargs`), a nehodnotit ho jako běžný poziční slovník.

---

## ⚙️ Architektonické principy

* **Jednoznačnost (Type Safety):** Odstraňuje riziko, že testovací engine zamění testovací slovník za běžnou datovou hodnotu.
* **Neměnnost (Immutability):** Objekt je po vytvoření zmrazen (`frozen=True`). To zaručuje, že testovací pipeline nemůže parametry během běhu omylem modifikovat (žádné vedlejší účinky).
* **Nativní rozbalování:** Díky implementaci protokolu `Mapping` můžete `Kwargs` kdekoli v Pythonu rozbalit pomocí standardního operátoru dvojité hvězdičky: `func(Kwargs(a=1))`.
* **Interní ochrana (Guard):** Pokud se pokusíte inicializovat `Kwargs` nevalidním způsobem (např. předáte více pozičních argumentů nebo objekt, který není slovníkem), interní validátor okamžitě vyhodí srozumitelnou výjimku a zastaví test dříve, než dojde k neočekávanému chování.

---

## 🛠️ Jak se používá

Třída dědí z `collections.abc.Mapping`, je **frozen** (neměnná) a podporuje dva způsoby bezpečné inicializace:

```python
from simplibs.exception.testing.tools import Kwargs

# 1. Definice pomocí inline pojmenovaných parametrů
invalid_params = Kwargs(timeout=10, strict=True)

# 2. Definice předáním existujícího slovníku
invalid_params = Kwargs({"timeout": 10, "strict": True})
```



## 🔍 Praktický příklad v testu

Představme si funkci, která přijímá klíčová slova (`kwargs`) a my chceme otestovat její selhání. Pomocí `Kwargs` předáme parametry naprosto jednoznačně:

```python
# Testovaná funkce
def validate_connection(**kwargs):
    if kwargs.get("timeout", 0) > 60:
        raise SimpleExceptionSettingsError(
            value=kwargs["timeout"],
            label="timeout",
            problem="Connection timeout cannot exceed 60 seconds."
        )

# Použití v testu s explicitním Kwargs
def test_validate_connection(subtests):
    assert_exception_function(
        subtests,
        validate_connection,
        invalid_params=Kwargs(timeout=99, strict=True), # Bezpečně se rozbalí jako **kwargs
        exception_type=SimpleExceptionSettingsError,
        value=99,
        label="timeout",
        problem="Connection timeout cannot exceed 60 seconds."
    )
```

---

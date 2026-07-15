### Soubor 1: `README.md` (Rychlá referenční karta)

# 📦 `testing/tools` — Pomocné nástroje pro strukturované testy

Balíček `testing/tools` obsahuje vysoce zaměřené pomocné nástroje a context managery, které sjednocují chování testovacích pipelines v knihovně `SimpleException`. Odstraňují syntaktickou zátěž a eliminují větvení kódu v testech.

> 💡 **Hledáte podrobný návod a kód nástrojů?** Přejdete na [Uživatelský průvodce s příklady](USER_GUIDE.md).

---

## ⚙️ Architektonické principy
- **Jednoznačnost** ➔ `Kwargs` jasně odděluje běžný slovník (hodnotu) od pojmenovaných parametrů.
- **Bezpodmínečnost** ➔ `maybe_subtest` odstraňuje nutnost psát v testech podmínky typu `if verbose:`.
- **Neměnnost (Immutability)** ➔ `Kwargs` je po vytvoření zmrazený (frozen), což zamezuje vedlejším efektům při testování.
- **Nativní integrace** ➔ Oba nástroje plně spolupracují s standardním ekosystémem Pytestu.

---

## 🧭 Přehled nástrojů

### 1. `Kwargs` (Sémantický wrapper)
Neměnný wrapper, který řeší typovou nejednoznačnost v Pythonu. Explicitně říká normalizační pipeline, že zabalený slovník se má rozbalit jako pojmenované argumenty (`**kwargs`), a ne jako jeden poziční argument typu `dict`.

### 2. `maybe_subtest` (Podmíněný context manager)
Elegantní adaptér nad `pytest-subtests`. Umožňuje jedním zápisem pokrýt jak detailní režim se subtesty (`verbose=True`), tak tichý/rychlý režim bez subtestů (`verbose=False`).

---

## 🔍 Rychlé příklady použití

### Použití `Kwargs` pro definici parametrů
```python
# Předání parametrů do testovací pipeline (rozlišení od běžného dictu)
invalid_params = Kwargs(timeout=10, strict=True)

# Použití jako nativní slovník (lze rozbalit pomocí **)
assert my_function(**Kwargs(timeout=10)) == {"timeout": 10}

```

### Použití `maybe_subtest` v testu

```python
# Pokud verbose=True -> vytvoří se subtest "vlastnost_xyz"
# Pokud verbose=False -> kód uvnitř se prostě standardně vykoná
with maybe_subtest(subtests, name="vlastnost_xyz", verbose=verbose):
    assert exc.label == "CHYBA"

```

```

---

### Soubor 2: `USER_GUIDE.md` (Uživatelský průvodce)

```markdown
# Uživatelský průvodce pro testovací nástroje (`testing/tools`)

Tento průvodce představuje dva klíčové nástroje, které udržují testovací kód v knihovně `SimpleException` čistý, čitelný a bez zbytečného větvení.

---

## 🧩 1. `Kwargs` — Vyřešení nejednoznačnosti slovníků

V Pythonu může slovník `{...}` reprezentovat dvě zcela odlišné věci:
1. **Hodnotu** (např. předáváte slovník jako jeden poziční argument `value`).
2. **Sadu parametrů** (které se mají do funkce předat jako `**kwargs`).

Při automatizovaném testování funkcí (např. v `bulk_test`) vzniká problém: *Jak má testovací engine poznat, zda je předaný slovník hodnota, nebo sada parametrů?*

Třída `Kwargs` funguje jako **sémantický štítek**. Jakmile slovník zabalíte do `Kwargs`, testovací pipeline okamžitě ví, že jej má rozbalit jako pojmenované argumenty.

### Jak se `Kwargs` používá:

Můžete jej inicializovat buď předáním hotového slovníku, nebo přímo jako pojmenované parametry:

```python
# Varianta A: Inicializace inline pojmenovanými parametry
params_inline = Kwargs(strict=True, limit=5)

# Varianta B: Inicializace předáním slovníku (Mapping)
params_dict = Kwargs({"strict": True, "limit": 5})

# Díky tomu, že Kwargs dědí z collections.abc.Mapping, se chová jako běžný dict
# a můžete ho kdekoli rozbalit pomocí operátoru **
print(params_inline["strict"])  # Vypíše: True
my_function(**params_inline)    # Funguje nativně v Pythonu!

```

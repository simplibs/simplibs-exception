# 📦 `SimpleExceptionData` — Pure Exception State Model

`SimpleExceptionData` je základní datová třída celé knihovny **SimpleException**.  
Reprezentuje čistý, izolovaný stav výjimky bez jakékoliv runtime logiky, formátování nebo MRO magie.

Je navržena tak, aby byla:

- **deterministická**,  
- **plně izolovaná**,  
- **bez vedlejších efektů**,  
- **snadno testovatelná**,  
- **jediným zdrojem pravdy** pro všechny výstupní režimy a serializace.

---

## 🧭 Účel třídy

`SimpleExceptionData` slouží jako:

- **pasivní datový model** pro `SimpleException`,  
- úložiště všech veřejných atributů výjimky,  
- zdroj dat pro serializaci (`to_dict`, `to_debug_dict`, `to_json`),  
- zdroj metadat pro výstupní režimy (PRETTY, SIMPLE, LOG, ONELINE),  
- místo, kde se provádí lazy stack tracing (`caller_info`).

Třída **neobsahuje žádnou aktivní logiku**:

- neprovádí normalizaci vstupů,  
- neřeší layout,  
- neřeší MRO,  
- neřeší formátování textu,  
- neřeší runtime mutace.

Všechny tyto části jsou řešeny v jiných balíčcích.

---

## 📁 Struktura atributů

### 🔹 Core metadata
- `error_name`: textová kategorie chyby  
- `exception`: zachycená cizí výjimka nebo její typ  
- `intercepted_exception`: textová stopa zachycené výjimky

### 🔹 Inspected value
- `value`: libovolný objekt, default `UNSET`  
  (musí být sentinel, protože `None` je validní hodnota)

### 🔹 Popis chyby
- `label`: název hodnoty  
- `expected`: očekávaný stav  
- `message`: hlavní textová zpráva  
- `problem`: popis problému  
- `context`: doplňující metadata

### 🔹 Náprava
- `how_to_fix`: instrukce pro uživatele

### 🔹 Tracing
- `get_location`: bool/int — hloubka stack tracingu  
- `skip_locations`: blacklist cest  
- `_cached_caller_info`: lazy cache pro stack metadata

### 🔹 Layout
- `oneline`: zda se má výjimka zobrazit v jedné řádce

---

## 🧩 Lazy stack tracing (`caller_info`)

`caller_info` je jediná aktivní vlastnost třídy.  
Je navržena tak, aby byla:

- **lazy** — provede stack scanning až při prvním použití,  
- **cached** — výsledek se uloží do `_cached_caller_info`,  
- **bezpečná** — nikdy nevyvolá výjimku,  
- **izolovaná** — používá pouze `extract_caller_info`.

Chování:

- pokud `get_location=False` → vrací `None`,  
- pokud je cache `UNSET` → provede stack scanning,  
- pokud je cache vyplněná → vrací uložený výsledek.

---

## 🔄 Serializace

### `to_dict()`
Vrací čistý dictionary obsahující pouze:

- veřejná business data,  
- hodnoty, které nejsou `UNSET`,  
- hodnoty, které mohou být `None`.

Neobsahuje:

- interní metadata,  
- layout konfigurace,  
- tracing metadata.

---

### `to_debug_dict()`
Rozšířený snapshot obsahující:

- vše z `to_dict`,  
- `caller_info`,  
- `intercepted_exception`,  
- `rendered_message` (pokud existuje).

Slouží pro:

- debugging,  
- telemetry,  
- crash dumpy.

---

### `to_json()`
Serializuje výstup `to_dict()` do JSON.  
Komplexní typy se převádějí přes `default=str`.

---

## 🔍 Příklady použití

### Základní instance
```python
data = SimpleExceptionData(
    label="user_id",
    expected="non-empty string",
    value=None,
)
```

### Získání místa vzniku chyby
```python
loc = data.caller_info
```

### Serializace
```python
payload = data.to_dict()
debug = data.to_debug_dict()
json_text = data.to_json()
```

---

## 🛡️ Architektonické principy

- **Čistá izolace**  
  Třída neobsahuje žádnou aktivní logiku mimo lazy tracingu.

- **UNSET sentinel**  
  Zajišťuje, že `None` je validní hodnota a neznamená „nevyplněno“.

- **Lazy caching**  
  Stack scanning se provádí pouze jednou.

- **Deterministická serializace**  
  Žádné dynamické introspekce, explicitní whitelist.

- **Bezpečnost**  
  Tracing nikdy nevyvolá výjimku.

---


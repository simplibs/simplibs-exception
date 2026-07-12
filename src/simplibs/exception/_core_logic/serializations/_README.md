# 📦 `_core_logic/serializations` — Exception Serialization Engine

Balíček `serializations` obsahuje interní nástroje pro převod výjimky do strukturovaných datových formátů.  
Je to čistě **datová vrstva**, která neřeší formátování textu, layout, tracing ani runtime logiku.  
Je navržena tak, aby byla:

- **deterministická**,  
- **bezpečná**,  
- **bez vedlejších efektů**,  
- **plně izolovaná od ostatních částí knihovny**,  
- **snadno testovatelná**.

---

## 🧭 Co tento balíček řeší?

### 1) Převod výjimky na dictionary (`to_dict`)
Slouží pro:

- logování,  
- API odpovědi,  
- jednoduché datové exporty,  
- uživatelské zobrazení bez interních detailů.

Výstup obsahuje pouze:

- veřejné business atributy (`label`, `message`, `expected`, …),  
- hodnoty explicitně nastavené uživatelem,  
- hodnoty, které nejsou `UNSET`.

Neobsahuje:

- interní runtime metadata (`caller_info`, `get_location`, `skip_locations`),  
- layout konfigurace (`oneline`),  
- nic, co by nemělo opustit knihovnu.

---

### 2) Rozšířený debug snapshot (`to_debug_dict`)
Slouží pro:

- interní diagnostiku,  
- telemetry systémy (Sentry, crash dumpy),  
- hlubší analýzu výjimky během vývoje.

Rozšiřuje `to_dict` o:

- `caller_info` — místo vzniku výjimky,  
- `intercepted_exception` — zachycená cizí výjimka,  
- `rendered_message` — finální textová podoba výjimky.

Je to jediný způsob, jak získat kompletní interní stav výjimky.

---

## 📁 Obsah balíčku

### `to_dict.py`
Funkce, která:

- explicitně mapuje veřejné atributy,  
- filtruje `UNSET`,  
- zaručuje, že interní metadata se nikdy neobjeví ve výstupu,  
- poskytuje stabilní API pro všechny výstupní režimy.

---

### `to_debug_dict.py`
Funkce, která:

- staví na `to_dict`,  
- přidává runtime metadata,  
- přidává finální renderovanou zprávu,  
- používá bezpečný `getattr` (žádné výjimky při neúplné inicializaci).

---

### `__init__.py`
Re-exporty pro čisté interní API.

---

## 🧩 Jak serializace zapadá do celého systému?

Serializace je propojena s:

- `SimpleExceptionData` (zdroj dat),  
- `SimpleException` (runtime logika),  
- výstupními režimy (které používají `to_dict` nebo `to_debug_dict`),  
- tracingem (který poskytuje `caller_info`).

Ale **není** propojena s:

- normalizačními funkcemi,  
- MRO logikou,  
- layout enginem,  
- settings meta validacemi.

Je to izolovaný modul, který řeší jedinou věc:  
**Jak převést výjimku na strukturovaná data.**

---

## 🔍 Příklady použití

### Základní dictionary
```python
exc = SimpleException("Boom", label="x")
payload = exc.to_dict()
```

Výstup obsahuje pouze veřejná data.

---

### Debug snapshot
```python
exc = SimpleException("Boom", label="x")
debug = exc.to_debug_dict()
```

Výstup obsahuje:

- veřejná data,  
- místo vzniku výjimky,  
- zachycenou cizí výjimku (pokud existuje),  
- finální renderovanou zprávu.

---

## 🛡️ Architektonické principy

- **Explicitní whitelist**  
  Žádná dynamická introspekce, žádné riziko leaků.

- **UNSET filtr**  
  Hodnoty, které uživatel nenastavil, se do výstupu nedostanou.

- **Bezpečný debug režim**  
  `to_debug_dict` nikdy nevyvolá výjimku.

- **Čistá izolace**  
  Serializace neřeší layout, tracing ani runtime logiku.

---

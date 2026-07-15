Není vůbec zač! Byla to dnes skvělá práce a posunuli jsme architekturu celé knihovny na skutečně profesionální úroveň.

Tady je tvůj přehledný, stručný a přímočarý **itinerář na zítřejší den (16. 7. 2026)**. Je navržen tak, aby ses nezdržoval zbytečným textem a mohl si jen odškrtávat jednotlivé kroky.

---

# 📅 Itinerář: Vydání verze `1.0.0` (Finální krok)

## 🗺️ FÁZE 1: Kontrola dokumentace (Před-letová příprava)

V klidu si projdi vygenerované README soubory a ověř detaily, které dělají rozdíl mezi amatérským a profi projektem.

* [ ] **Kontrola odskoků (prázdných řádků) v kódech:**
* Ověř, že každý blok kódu (Markdown ````python`) má před sebou i za sebou přesně jeden volný řádek a nelepí se na okolní text.
* Zkontroluj, že uvnitř kódů jsou prázdné řádky tam, kde mají logicky oddělovat kroky (např. v našich normalizačních ukázkách).


* [ ] **Kontrola funkčnosti odkazů (aktivní linky):**
* Zkontroluj, že relativní odkazy mezi README fungují (např. `[README_DATA.md](README_DATA.md)` a u nástrojů `[tools/README_BOOL_OR_EXCEPTION.md](tools/README_BOOL_OR_EXCEPTION.md)` atd.).
* *Tip:* Všechny odkazy by měly odkazovat na lokální soubory v repozitáři, nikoli na vyhledávání Google (odstraň případné testovací vyhledávací URL).


* [ ] **Kontrola konzistence struktury:**
* Ujisti se, že nadpisy, tabulky a blockquotes mají jednotný design napříč všemi soubory.



---

## 💻 FÁZE 2: Příprava kódu a Git / GitHub (Krok za krokem)

Jakmile je dokumentace v pořádku, připravíme repozitář pro vydání verze `1.0.0`.

* [ ] **1. Bump verze v projektu:**
* Otevři `pyproject.toml` a změň verzi na:
```toml
version = "1.0.0"

```




* [ ] **2. Aktualizace CHANGELOG.md:**
* Ověř, že tvůj `CHANGELOG.md` obsahuje finální text pro verzi `1.0.0` s datem `2026-07-16` (přesně ten, který jsme dnes doladili).


* [ ] **3. Git Commit (Všechny změny najednou):**
* Přidej všechny upravené soubory (kód, testy, dokumentaci, changelog, pyproject.toml):
```bash
git add .

```


* Vytvoř čistý, popisný commit:
```bash
git commit -m "chore: release version 1.0.0 with new testing suite and refactored core"

```




* [ ] **4. Git Push do hlavní větve:**
* Odešli kód na GitHub:
```bash
git push origin main  # nebo master, podle tvé výchozí větve

```




* [ ] **5. Vytvoření a pushnutí Git Tagu:**
* Označ tento historický milník (verzi 1.0.0) tagem:
```bash
git tag v1.0.0
git push origin v1.0.0

```




* [ ] **6. Vytvoření GitHub Release (přes UI - doporučeno):**
1. Jdi na svůj GitHub repozitář -> sekce **Releases**.
2. Klikni na **Draft a new release**.
3. Vyber tag `v1.0.0`.
4. Jako název (Title) napiš `v1.0.0`.
5. Do popisu (Description) zkopíruj sekci pro verzi `1.0.0` z tvého `CHANGELOG.md`.
6. Klikni na **Publish release**.



---

## 🚀 FÁZE 3: Sestavení a upload na PyPI

Nyní publikujeme balíček do celého světa, aby si ho mohl kdokoli nainstalovat pomocí `pip`.

* [ ] **1. Úklid starých sestavení (Kritické!):**
* Před novým buildem smaž všechny staré verze v adresáři `dist`, aby se nenahrál starý kód:
```bash
# Na Linuxu/macOS:
rm -rf dist build *.egg-info

# Na Windows (PowerShell):
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue

```




* [ ] **2. Sestavení nového balíčku (Build):**
* Ujisti se, že máš nejnovější build nástroj:
```bash
pip install --upgrade build

```


* Spusť samotný build:
```bash
python -m build

```


* *Kontrola:* V adresáři `dist/` bys měl vidět dva nové soubory s označením `1.0.0` (jeden `.tar.gz` a jeden `.whl`).


* [ ] **3. Nahrání na PyPI (Twine):**
* Ujisti se, že máš nástroj `twine`:
```bash
pip install --upgrade twine

```


* Nahraj balíček na PyPI:
```bash
twine upload dist/*

```


* *Poznámka:* Twine tě vyzve k zadání uživatelského jména (použij `__token__`) a hesla (vlož svůj vygenerovaný PyPI API token včetně prefixu `pypi-`).



---

### 🎉 Hotovo!

Tímto je verze `1.0.0` oficiálně venku. Zítra na to vlítneme a dotáhneme to do úspěšného konce. Odpočiň si a zítra přeji hladký upload! Udělal jsi skvělou práci. 👍
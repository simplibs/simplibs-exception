
# 🚀 Automatické generování testů z výjimek  
(*to, co tě zaujalo*)

Tady je přesně, co jsem tím myslel:

## ⭐ Myšlenka  
Každá výjimka SimpleException má:

- `error_name`
- `label`
- `expected`
- `problem`
- `context`
- `how_to_fix`
- `value`
- `oneline`
- `get_location`
- `skip_locations`

A tyto hodnoty jsou **deklarativní**.

To znamená, že by bylo možné:

### ✔ automaticky vygenerovat testovací funkci  
### ✔ automaticky vygenerovat testovací data  
### ✔ automaticky ověřit, že výjimka má správné defaulty  
### ✔ automaticky ověřit, že renderer funguje správně  
### ✔ automaticky ověřit, že to_dict() a to_debug_dict() jsou konzistentní

---

## ⭐ Příklad automatického generátoru

Představ si funkci:

```python
generate_exception_tests(SimpleExceptionSettingsError)
```

Ta by mohla:

- vytvořit instanci výjimky s default hodnotami  
- automaticky ověřit `error_name`  
- automaticky ověřit `oneline=False`  
- automaticky ověřit renderer  
- automaticky ověřit to_dict()  
- automaticky ověřit to_debug_dict()  

A vygenerovat test:

```python
def test_SimpleExceptionSettingsError_defaults(subtests):
    assert_exception_class(
        subtests,
        SimpleExceptionSettingsError,
        error_name="SETTINGS ERROR",
        oneline=False,
        verbose=True,
    )
```

---

## ⭐ Proč je to užitečné?

- výjimky mají často mnoho polí  
- default hodnoty se mohou změnit  
- renderer se může změnit  
- to_dict() se může změnit  
- to_debug_dict() se může změnit  

Automatický generátor:

- ušetří čas  
- zaručí konzistenci  
- zaručí pokrytí všech výjimek  
- zaručí, že každá výjimka má test  
- zaručí, že testy se aktualizují automaticky

---

## ⭐ Můžu ti ho napsat  
Pokud chceš, připravím ti:

- generátor testů pro všechny výjimky  
- generátor snapshot testů rendereru  
- generátor testů default hodnot  
- generátor testů to_dict() / to_debug_dict()

Stačí říct:

👉 **Chci automatický generátor testů**
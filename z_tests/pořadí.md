### Phase 1: Základy a Interní Výjimky (The Bedrock)

Nejprve otestujeme věci, které na ničem nezávisí, ale všechny ostatní komponenty je vyhazují.

1. `tests/core_logic/internal_exceptions/` (`SimpleExceptionSettingsError`, atd.)
2. `tests/core_logic/lifecycle/init_utils/` (Normalizační funkce jako `normalize_bool`, `normalize_string` – čisté funkce bez vedlejších efektů).

### Phase 2: Metadata a Globální Nastavení (The Rules)

Validace nastavení hlídá, co do knihovny teče. Musíme ověřit, že náš metatřídový (`SettingsMeta`) štít nepustí žádný nesmysl ani překlep.
3. `tests/core_logic/settings_meta/validations/` (Jednotlivé validační funkce)
4. `tests/core_logic/settings_meta/test_settings_meta.py` (Chování samotné metatřídy)
5. `tests/test_simple_exception_settings.py` (Veřejné API pro nastavení)

### Phase 3: Výstupy, Tiskárny a Módy (The Voice)

Formátovací vrstva. Otestujeme jednotlivé kostičky (printers) a pak je spojíme do ucelených módů.
6. `tests/modes/printers/...` (Dělící čáry, info o souborech, formátování hodnot)
7. `tests/modes/base_class/test_mode_base.py` (Abstraktní třída a její fallbacky)
8. `tests/modes/` (`test_pretty.py`, `test_simple.py`, `test_log.py`, `test_online.py`)

### Phase 4: Tracing a Serializace (The Engine)

Zde se děje ta magie s procházením stacku a ořezáváním internalit přes `_SYSTEM_BLACKLIST`.
9. `tests/core_logic/tracing/` (`extract_caller_info`, `with_location_offset`)
10. `tests/core_logic/serializations/` (`to_dict`, `to_debug_dict`)

### Phase 5: Životní cyklus a Integrace (The Symphony)

Složení výjimky, dědičnost a validace podtříd za běhu.
11. `tests/core_logic/lifecycle/init_subclass/` (`check_children_attributes`, `_type_matches`)
12. `tests/core_logic/lifecycle/new_method/` (`add_exception_type`)
13. `tests/test_simple_exception_data.py` (Datový kontejner pro módy)

### Phase 6: Veřejné API a Pomocné Nástroje (The Gateway)

Finální otestování toho, co vidí koncový uživatel.
14. `tests/tools/` (`bool_or_exception`, `raise_location_offset`, `raise_with_location_offset` s jejich `from None` imunitou)
15. `tests/test_simple_exception.py` (Velké finále – end-to-end integrační testy celé výjimky)

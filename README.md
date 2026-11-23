# DnD Games

Trvalé úložiště pro více nezávislých stolních RPG kampaní hraných s ChatGPT jako DM. Výchozím jazykem je čeština.

## Spuštění a pokračování

1. Načti `AGENTS.md` a `campaigns/index.json` z větve main.
2. Zvol přesný identifikátor kampaně. Načti její `state.json`, `rules.md`, `history.md`, `knowledge.md` a poslední událost.
3. Při prvním obnovení stručně ověř výchozí stav, zvláště označené rozpory. Pokračuj až na pokyn hráče.
4. Po každém vyhodnoceném tahu ulož nový checkpoint podle `system/protocol.md`. Neměň předchozí události.

## Kampaně

| ID | Hra | Stav |
| --- | --- | --- |
| dawnstar-rudolf | Elite Dangerous: Dawnstar | Importováno, den 18 |
| dawnstar-agent | Elite Dangerous: AGNT-06 | Importováno, samostatná kontinuita |

## Git

`main` je kanonická větev živé hry. `develop` je vývoj infrastruktury. Herní checkpointy ukládej atomicky na main, nikoli do vývojové větve. Před vývojem synchronizuj develop s main, při slučování zachovej novější herní stav. Nikdy nepřepisuj historii násilím.

Repozitář je veřejný. DM podklady, neodhalená tajemství a původní neprověřené soubory zůstávají mimo veřejný Git. Adresář `local_sources/` je ignorován. Veřejné checkpointy obsahují jen zjištěné herní skutečnosti, nikoli neveřejné plánované zvraty.

Kontrola lokálně: `python3 tools/validate.py`. Testy: `python3 -m unittest discover -s tests`. Samotná hra nevyžaduje běžící server ani externí knihovny. GitHub konektor používá přímé čtení a zápis souborů.

# Protokol trvalého kontextu v1

## Autorita dat a načítání

Aktuální checkpoint `state.json` je zdroj pro stav v okamžiku posledního uloženého tahu. Historie a události jsou zdrojem pro konkrétní uskutečněné akce a objevy. Při rozporu mezi staršími exporty a pozdější přímou událostí má přednost doložená pozdější událost; rozdíly se evidují. Pro historické importy platí zvláštní poznámky v `sources.md`. Nezjištěný stav není nula.

1. Načti main a zapamatuj SHA hlavy. Načti AGENTS, registry a soubory zvolené kampaně ze stejného SHA.
2. Načti stav a poslední event, případně další relevantní události. Čti pravidla, historii a znalosti podle scény. Nepoužívej vývojovou větev jako savegame.
3. Zkontroluj revizi, polohu, herní den, pending, stav postav, aktivní úkoly, techniku a důkazy. Při nezavřeném hodu pokračuj právě tímto hodem; znovu nevyhodnocuj předchozí akci.
4. Hráč má poslední slovo o úmyslu vlastní postavy. Při nejasnosti polož konkrétní otázku, pokud by omyl měl nevratný důsledek.

## Transakce

Každá změna kanonického stavu zvyšuje `revision` přesně o 1. Vytvoř nový soubor `events/NNNNNN.json` s předchozí a novou revizí, akcí hráče, odpovědí DM, skutečnými hody, změnami, zdroji a případnou opravou předchozího záznamu. První import je event 000000. Čistě OOC dotaz beze změny stavu nemusí vytvořit event. Čekání na hod je změna pending a může být samostatným checkpointem.

Ve stejném commitu nahraď pouze `state.json` nové revize a dle potřeby doplň `knowledge.md` nebo `history.md`. Historické záznamy neměň; korekce jsou nové události. `state.json` musí být kompletní snapshot, nikoli delta. Nikdy nesnižuj revizi a nemaž eventy.

Na GitHubu vytvoř tree ze stávajícího tree SHA, commit s rodičem rovným načtené hlavě a posuň main bez force s expected_sha. Ověř výsledný ref a nový stav. Při konfliktu žádné force push. Jednoznačný commit message: `game(<id>): checkpoint <revision>`. Pro přechod mezi kampaněmi načti vždy jejich vlastní stav.

## Viditelnost a znalosti

`knowledge.md` rozlišuje pozorování, tvrzení NPC a systémy, hypotézy, otevřené otázky. Fikční dokumenty mohou lhát. Přístupová práva hráče a NPC se neslučují. Skryté DM podklady se drží mimo veřejný repozitář (případné samostatné soukromé úložiště je nutno skutečně připojit). Hra nevyžaduje, aby hráč četl soubory DM.

## Selhání a obnova

Když GitHub není dostupný, nevydávej stav za uložený. Předlož přenosný checkpoint a event s původní očekávanou revizí. Při obnovení konektoru načti main, porovnej revize a uložené události. Neprováděj stejný tah podruhé. Restart nového chatu nemá měnit stav.

## Více kampaní

Každá kampaň má vlastní pravidla, snapshot, historii, znalosti, zdroje a eventy. Přidání nové kampaně znamená nový jedinečný slug v registry a založení kopie šablony. Sdílené lore je jen reference, nikdy sdílený herní stav. Při práci nad develop se nevyvíjí ani neposouvá děj.

## Modulární layout 2

Pokud state.layout_version je 2, state.json zůstává úplným manifestem snapshotu. Objekty ref, sheet_ref a inventory_ref odkazují na relativní JSON soubory uvnitř kampaně. roster_ref a inventory_refs jsou další explicitní odkazy. Všechny JSON moduly mají schema_version 1, campaign_id, id a kind. Odkazované soubory čti ze stejného SHA, nikoli z různých hlav. Kanonická data jsou v modulu, nikoli paralelní inline kopii; historická metadata jsou označena. Ulož state, event a všechny skutečně změněné moduly atomicky ve stejném commitu. Neměň modul, který se v daném tahu nezměnil. Pro aktuální scénu čti pouze nutné moduly; pro audit lze načíst celý graf. audit_ref označuje Markdown audit a není JSON modul. Poslední administrativní event může mít last_gameplay_event; při obnově scény čti i tento event. Pokud některý modul chybí či má jinou identitu, nepokračuj s odhadem. Validátor podporuje původní inline layout i modulární layout.

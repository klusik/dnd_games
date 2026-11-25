# Revize kontinuity, inventářů a sheetů, checkpoint 30

Den 19, administrativní revize bez posunu hry. Předchozí stav je přesně zachován v commitu a198fe1c8a30c0d24efb7a48dce1f71a7a5158df; events/000000.json až events/000029.json nebyly měněny.

## Rozsah a zdroje

- Přímý původní log ChatGPT log.txt, 16 844 řádků, SHA256 e3c11725d41f2737f75261a950d3b6778c582b3d7d465ad6e6122570a57d9667. Prošel systematickým vyhledáním atributů, levelů, zdraví, výstroje, zásob, spotřeb, oprav, postav a zařízení, s kontrolou příslušných pasáží v kontextu. Nejde o strojový důkaz, že každý implicitně zmíněný předmět je zachycen.
- Porovnány dostupné historické exporty Rudolfa, zejména nejnovější rudolf_dawnstar_updated.txt a dřívější verze s totožnými devíti skilly. Dny 16 až 18 pouze rozšířený save.
- Načteno všech 30 dosavadních eventů z main při revizi 29; návaznost 0 až 29 ověřena.
- Samostatná kampaň AGNT-06, Foxen/Pavel a společné neveřejné DM materiály nebyly přimíchány. Plné osobní jméno z fikčního archivu se nezveřejňuje. Zdrojové ZIPy zůstávají mimo veřejný Git.

## Rozpory a rozhodnutí

| Oblast | Historický nález | Rozhodnutí pro hru |
|---|---|---|
| Rudolf HP | 12 na začátku, +4 ale uvedeno 14 na levelu 2; další číselný údaj nezjištěn | 14/14 jako explicitní konzervativní prospektivní baseline po již odehraném odpočinku, nikoli historické potvrzení |
| Rudolf AC | 13 za lehkou kombinézu; nová hodnota EVA nedoložena | 13 jako prozatímní baseline, bez dvojitého bonusu |
| Rudolf skilly | Starší level 3 Tech +7, Inv +6, Eng +7, Piloting +5; novější level 4/5 hodnoty nižší, Stealth +4 navzdory deklarovanému +1 | Platí nejnovější opakované hodnoty 6/5/4/4/4/4/4/2/1, nikoli nové přepočítání |
| Proficiency | Level 2 explicitně +2 | Současné celkové skill bonusy již nepřepočítávat. U nespecializovaných atributových hodů relevantní atribut |
| Data Whisperer | +2 na starou tech/databáze; také různé formulace bonusu a výhody | +2 relevantní staré tech/databáze/šifry/datové signály, advantage proti digitálním klamům. Nepřidávat plošně další výhodu |
| Level 2 | Technické soustředění a Skenovací čtení skutečně uděleny | Obnoveny, dnes nepoužity podle doložených tahů |
| Level 5 a DS-01 | Bioanalytik a Resonant Recall potvrzeny | Zachovány |
| Kařina noha | Zlomenina levého femuru, ošetřena; pozdější samostatná chůze, bez výslovného měření zhojení | Bez aktuálního automatického postihu. Zdravotní historie oddělena od mechanické baseline |
| Kara a Δ-47 | Číselné sheety nebyly doloženy | Prospektivní DM baseline v samostatných profilech. Nepřisuzovat tyto hodnoty minulým scénám |
| Munice | Rudolf cca 20 v úvodu, žádná doložená střelba; Kara aktuálně zbraň připravena, typ a munice neznámy | Rudolf 20 jako odhad pro hru; Kara 12 jako výslovně nová DM baseline. Nejde o nalezení ani doplnění zásob |
| Dron | 6 h výdrž v úvodu, později mikroreaktor; původně bez zbraní, později EMP, pohyb nohy vs popisy letu | Zachovat oba historické údaje, aktuální výdrž a přesný pohon neznámé. EMP obranný, bez automatického damage. Pouze jeden instalovaný upgrade |
| Výstroj a zásoby | Četné nálezy, použití a přesuny, ale chybějící souvislý ledger spotřeby | Historické množství není současný zůstatek. Stav položek a provenance explicitně evidovány. Nedoložené vzorky a nevyzvednutý satelit nejsou k dispozici |
| Přístup k DS-03 | Otevřena závora a hlavní dveře, nikdo ještě nevstoupil | Scéna beze změny, žádný nový hod či odhalení |
| Registry | paused versus state active | Sjednoceno na active pouze u této kampaně |

## Pravidla práce s daty

Aktivní sheety: characters/rudolf.json, kara.json, delta-47.json, gamma-six.json. Doložené nepřítomné osoby a systémy: characters/archival.json. Osobní inventáře, expediční inventář, 4B a data v inventories/. Technický stav vozidel v assets/. Detail polohy a průzkumu v world/. state.json je úplný manifest aktuálního snapshotu včetně odkazů, které musejí být načteny ze stejného commitu. Neupravuj staré eventy.

### Stavy položek

equipped/carried/confirmed: potvrzené v aktuální situaci nebo přímém současném stavu; last_known: poslední doložená evidence, může vyžadovat ověření umístění; provisional: číselný herní odhad nebo DM baseline; historical_unverified: historický nález, dnešní dostupnost neověřena; used: spotřebované nebo použité, neznovuzískat; installed: součást zařízení, ne volný předmět; not_acquired: nezískané. null znamená neznámé, nikoli 0. Při spotřebě zaznamenej skutečnou položku, množství a zdroj. Fyzické a digitální kopie jsou různé kategorie, nesčítat je. Historické metadata v souborech nejsou druhý inventář. Žádný nové přesné množství nepřidávej bez odhalení nebo výslovného pravidla.

## Dřívější záznam nejistot

- Přímý export končí dnem 15; dny 16 až 18 jsou z pozdějšího savegamu. Den 18 je nejnovější doložený checkpoint, ne nutně poslední skutečně odehraný tah.
- Přesné HP, maximální HP, AC, zásoby, energie, munice, čas a aktuální poloha DBE nejsou v pozdním save uvedeny.
- DS-03 má několik odlišných souřadnic a vzdáleností; evidovat, nepřepočítávat bez průzkumu.
- Úvod přímého logu začíná ve vraku; souhrny začínají na základně. Přímá scéna má pro úvod přednost.
- Deník naznačuje záměr odjet k DS-03 zítra, nejnovější save končí u SRV po hovoru Kaře. Příjezd do 4B ani další noc nepotvrzeny.
- Oprava importu: původní přímý log identifikuje planetu Gliese 5206 c, nikoli HIP 22022. Některé interní briefingy používají označení Moon 4B / Pleiades-South a HIP 20491; jde o údaje z fikčních dokumentů, nikoli nové astronomické určení aktuální polohy.
- Výpis GAMMA status ACTIVE FOR 674 DAYS se liší od pozdějšího záznamu aktivace dva hodiny před havárií. Význam obou časů zatím nerozhodnut; nedoplňovat vysvětlení bez zjištění.

## Rozhodnutí o hratelných hodnotách

Toto je jednorázové administrativní doplnění na žádost hráče, nikoli hraná scéna. Pro aktivní postavy jsou čísla, která se nedala obnovit, označena jako provisional_play_baseline / provisional_dm_baseline nebo provisional. Rudolfův poslední doložený HP údaj a AC byly použity konzervativně. Kara a dron mají navržené funkční hodnoty odpovídající rolím. Žádné levely, XP, předměty ani nové schopnosti nad rámec doložených grantů a výslovně popsaných mechanických výchozích hodnot se nepřidělují. Mimo aktivní družinu nejsou uměle vytvořené statblocky. Pokud hráč poskytne původní přesný sheet, má přednost a oprava bude nový event.

# Nová kampaň

Zvol jedinečný slug, např. space-exploration. Založ `campaigns/<slug>/` se state.json a events/000000.json podle šablon, nastav campaign_id v obou a doplň rules.md, history.md, knowledge.md, sources.md. Přidej ji do registry. Nevyplňuj údaje neznámé postavy bez podkladu. Události od 000001 vyžadují previous_revision odpovídající předchozímu číslu. Pro čekání na hod používej scene.pending jako objekt, např. {"kind":"roll","skill":"Technology","dice":"1d20","modifier":6,"dc":15,"action":"Analyzovat terminál"}. Po výsledku zruš pending a zapiš roll s raw, modifier, total a DC.

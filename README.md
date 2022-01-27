
PROJEKT 3 – Elections Scraper
Výsledkem tohoto projektu je skript, který vybere jakýkoliv územní celek z odkazu : https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xnumnuts=2102, a díky němuž můžeme vyscrapovat výsledky hlasování pro všechny obce.

POSTUP VYPRACOVÁNÍ PROJEKTU:
Instalace potřebných knihoven. Instalovány přímo ve virtuálním prostředí PyCharmu.
Hlavní funkce ověřuje zadané argumenty (URL adresu a název souboru. Data uloží do .csv souboru a uloží. Pokud je jeden z argumentů zapsán špatně, program by ho měl na tuto skutečnost upozornit.
Výstupem bude soubor .csv – tabulka, která bude obsahovat požadované informace o volbách ve vybraném okrese: kód obce, název obce, voliči v seznamu, vydané obálky, platné hlasy, kandidující strany.

SPUŠTĚNÍ PROGRAMU POMOCÍ 2 ARGUMENTŮ:

>python3 "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xnumnuts=2102" "Results.csv"

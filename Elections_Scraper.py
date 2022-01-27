import requests
from bs4 import BeautifulSoup
import csv
import sys


def main(url: str, jmeno_souboru: str) -> None:
    zadana_url(url)
    zadany_nazev(jmeno_souboru)
    print(f'Přístupova URL adresa: {url}')
    okres_tab = tab_z_url(url)
    status = zapis_do_csv(okres_data(okres_tab), jmeno_souboru)
    print(status)


def zadana_url(text: str) -> None:
    if 'https://volby.cz/pls/ps2017nss/' not in text:
        print('Neplatná URL adresa.')
        exit()
    elif 'https://volby.cz/pls/ps2017nss/ps31?' not in text:
        print('První argument musí být URL adresa.')
        exit()
    elif '.csv' in vstupni_url:
        print('První argument musí být URL adresa.')
        exit()


def tab_z_url(url):
    try:
        odpoved = requests.get(url)
        odpoved.raise_for_status()
    except requests.ConnectionError:
        print('Špatné spojení.')
        exit()
    else:
        pol = BeautifulSoup(odpoved.text, 'html.parser')
    return pol.find_all('table')


def okres_data(okres_tabl: 'bs4.element.ResultSet') -> list:
    vysledek = []
    for tabl in okres_tabl:
        tabl_trs = tabl.find_all('tr')
        for tr in tabl_trs[2:]:
            row_tds = tr.find_all('td')
            if row_tds[0].text != '-':
                row_href = row_tds[0].find('a').get('href')
                mun_tab = tab_z_url(
                    f'https://volby.cz/pls/ps2017nss/' + row_href
                )
                vysledek.append({
                    **zaklad_data(row_tds),
                    **info_volici(mun_tab),
                    **hlasy(mun_tab)
                })
    return vysledek


def zadany_nazev(nazev: str) -> None:
    if '.csv' not in nazev:
        print('Výstupem musí být CSV soubor')
        exit()


def info_volici(tables) -> dict:
    info = {}
    table_trs = tables[0].find_all('tr')
    row_tds = table_trs[2].find_all('td')
    info['Voliči v seznamu'] = row_tds[3].getText().replace('\xa0', '')
    info['Vydané obálky'] = row_tds[4].getText().replace('\xa0', '')
    info['Kandidující strany'] = row_tds[5].getText()
    info['Platné hlasy'] = row_tds[7].getText().replace('\xa0', '')
    return info


def zaklad_data(row_tds: 'bs4.element.ResultSet') -> dict:
    return {
        'Kód obce': row_tds[0].getText(),
        'Název obce': row_tds[1].getText(),
    }


def hlasy(tabulky) -> dict:
    hlas = {}
    for tabl in tabulky[1:]:
        tabl_trs = tabl.find_all('tr')
        for tr_tag in tabl_trs[2:]:
            row_tds = tr_tag.find_all('td')
            strany = row_tds[1].getText()
            if strany != '-':
                hlas[strany] = row_tds[2].getText().replace('\xa0', '')
    return hlas


def zapis_do_csv(data: list, jmeno_souboru: str) -> str:
    try:
        csv_soubor = open(jmeno_souboru, mode='w', encoding='utf-8', newline='')
        sloupce = data[0].keys()

    except IndexError:
        print('Něco se pokazilo. Zkontrulujte vsupní adresu')
        exit()
    except AttributeError:
        print('Něco se pokazilo. Zkontrulujte vsupní adresu')
        exit()
    else:
        vstup = csv.DictWriter(csv_soubor, fieldnames=sloupce)
        vstup.writeheader()
        vstup.writerows(data)
        return f'Uloženo v souboru: {jmeno_souboru}'
    finally:
        csv_soubor.close()


try:
    vstupni_url = sys.argv[1]
    vstupni_soubor = sys.argv[2]
except:
    print('Musí být zadany dva argumenty: vstupní URL adresa a jméno souboru')
    exit()


if __name__ == "__main__":
    main(vstupni_url, vstupni_soubor)
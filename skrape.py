import requests
import os
from bs4 import BeautifulSoup as bs
import csv
import time


URL="https://www.ss.lv/lv/transport/cars/today-5/sell/"
LAPAS="lapas/"
DATI="dati/"


# 1. solis - saglabājam lapu lokāli
def saglaba(url, datne):
    """Saglabā dotas saites saturu html datnē

    Args:
        url (string): lapas adrese (URL)
        datne (string): datnes nosaukums
    """
    rezultats = requests.get(url)
    print(rezultats.status_code)
    if rezultats.status_code == 200:
        with open(datne, 'w') as f:
            f.write(rezultats.text)


# saglaba(URL, LAPAS + "pirma.html")


# 2. solis - izvelkam informāciju no lapas
def info(datne):
    """Izvelk infomāciju par auto no iepriekš saglabātas ss.lv lapas

    Args:
        datne (string): ceļš uz datni, piemēram "lapas/a1.html"

    Returns:
        array: Masīvs ar vārdnīcam, kas satur no lapas izvilktos auto datus
    """
    dati = []
    with open(datne, 'r') as f:
        html = f.read()
    
    zupa = bs(html, 'html.parser')
    # atrodam id="page_main"
    galvena = zupa.find(id='page_main') 
    # atrodam table zem tā
    tabulas = galvena.find_all("table")

    # trešā tabula ir tā, kur ir auto informācija
    rindas = tabulas[2].find_all("tr")

    # pirmā rinda ir kolonnu nosaukumi, izlaižam
    for rinda in rindas[1:]:
        # katrā rindā (t.i. katram auto) 
        # atrodam visas tabulas šūnas - tur ir attiecīgā info
        lauki = rinda.find_all("td")

        # # testa nolūkos izdrukā
        # for l in lauki:
        #     print(l)
        #     print("---------")
        try:
            # nav pareizs lauku skaits, izlaižam
            if (len(lauki) < 8):
                continue
            auto = {}
            auto["saite"] = lauki[1].find("a")["href"]
            auto["bilde"] = lauki[1].find("img")["src"]
            # izvācam jaunas rindas simbolus
            auto["apraksts"] = lauki[2].find("a").text.replace("\n", " ")
            # dažāds formatējums
            if lauki[3].b:
                if lauki[3].b.br:
                    lauki[3].b.br.replace_with(' ')
                auto["marka"] = lauki[3].b.text
            else:
                if lauki[3].br:
                    lauki[3].br.replace_with(' ')
                auto["marka"] = lauki[3].text
            auto["razotajs"] = auto["marka"].split(" ")[0]
            auto["gads"] = lauki[4].text
            # izvelkama dzinēja tipu no tilpuma lauka
            dzinejs = lauki[5].text
            if dzinejs[-1] == "D":
                auto["dzinejs"] = "Dīzelis"
                auto["tilpums"] = dzinejs[:-1]
            elif dzinejs == "E":
                auto["dzinejs"] = "Elektro"
                auto["tilpums"] = 0
            else:
                auto["dzinejs"] = "Benzīns"
                auto["tilpums"] = dzinejs
            # pārvēršam par skaitlisku vērtību
            if not lauki[6].text =="-":
                auto["nobraukums"] = lauki[6].text.replace(" tūkst.","")
            else:
                auto["nobraukums"] = 0
            # pārvēršam par skaitlisku vērtību
            auto["cena"] = int(lauki[7].text.replace("  €", "").replace(",",""))
            dati.append(auto)
        except Exception as e:
            print("Slikts sludinājums, trūkst datu")
            print(e, lauki)
    return dati


def saglaba_datus(dati):
    with open(DATI+'ss_auto.csv', 'a') as f:
        lauku_nosaukumi = ['razotajs', 'marka', 'gads', 'dzinejs', 'tilpums', 'nobraukums', 'cena', 'apraksts', 'bilde', 'saite']
        w = csv.DictWriter(f, fieldnames=lauku_nosaukumi)
        w.writeheader()
        for auto in dati:
            w.writerow(auto)

# info(LAPAS + "pirma.html")


def atvelkam_lapas(cik):
    # pirmajai lapai ir savādāka adrese
    url = "https://www.ss.lv/lv/transport/cars/today-5/sell/"
    saglaba(url, "{}page1.html".format(LAPAS, i))
    time.sleep(1)

    for i in range(cik):
        url = "https://www.ss.lv/lv/transport/cars/today-5/sell/page{}.html".format(i)
        saglaba(url, "{}page{}.html".format(LAPAS, i))
        time.sleep(1)



def izvelkam_datus():
    visi_dati = []
    for i in range(1, 21):
        datne = "{}page{}.html".format(LAPAS, i)
        
        datnes_dati = info(datne)
        visi_dati += datnes_dati
    saglaba_datus(visi_dati)


# # solis 3
# atvelkam_lapas(cik)
# # solis 4
# izvelkam_datus()
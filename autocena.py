import argparse
import sys
from termcolor import colored as cl
from lineara_regresija import ieladet_modeli, prognozejam_rezultatu


def ievade():
    turpinam = True
    modelis = ieladet_modeli("ss-modelis.pickle")
    print(cl("Auto cenu prognoze. Ievadiet pieprasītos datus, lai saņemtu prognozi.", "green", attrs=["reverse"]))
    while turpinam:
        gads = int(input("Auto izlaišanas gads vai 0, lai izietu: "))
        if gads == 0:
            turpinam = False
            continue
        tilpums = float(input("Dzinēja tilpums: "))
        nobraukums = float(input("Nobraukums, tūkstošos km.: "))
        dati = [[gads, tilpums, nobraukums]]
        prognoze = prognozejam_rezultatu(modelis, dati)
        print("Prognozētā cena:", cl(round(prognoze[0]), "green", attrs=["bold"]))
        print()


def main():
    if len(sys.argv)  < 3:
        ievade()
    else:
        parser = argparse.ArgumentParser(prog = 'autocena',
        description = """Nosaka auto cenu, izmantojot uz reāliem datiem trenētu modeli""")
        parser.add_argument('gads')
        parser.add_argument('tilpums')
        parser.add_argument('nobraukums')
        args = parser.parse_args()
        print(args)
        dati = [[args.gads, args.tilpums, args.nobraukums]]
        modelis = ieladet_modeli("ss-modelis.pickle")
        prognoze = prognozejam_rezultatu(modelis, dati)
        print("Prognozētā cena:", cl(round(prognoze[0]), "green", attrs=["bold"]))
  


if __name__ == "__main__":
    main()
import argparse
from termcolor import colored as cl
from lineara_regresija import ieladet_modeli, prognozejam_rezultatu


def prognozejam(dati):
    print("Ielādējam modeli no datnes")
    modelis = ieladet_modeli("ss-modelis.pickle")
    prognoze = prognozejam_rezultatu(modelis, dati)
    print(cl("Prognozētā cena:{}".format(prognoze[0]), "green", attrs=["bold"]))


def main():
    parser = argparse.ArgumentParser(prog = 'autocena',
        description = """Nosaka auto cenu, izmantojot uz reāliem datiem trenētu modeli""")
    parser.add_argument('gads')
    parser.add_argument('tilpums')
    parser.add_argument('nobraukums')
    args = parser.parse_args()
    print(args)
    dati = [[args.gads, args.tilpums, args.nobraukums]]
    prognozejam(dati)


if __name__ == "__main__":
    main()
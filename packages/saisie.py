MAX_QUOTE_BG = 20000


def query_battletag() -> str:
    while True:
        response = input("Quel est le compte recherché : ")
        if valide_iuk(response):
            return response


def query_int_value_min_max(texte: str, imin: int, imax: int) -> int:

    while True:
        try:
            response = int(input(f"{texte} (entre {imin} et {imax}) : "))
            if 0 < response < MAX_QUOTE_BG and valide_iuk(str(response)):
                return response
            else:
                print(f"Entrez un nombre entier compris entre {imin} et {imax}.")

        except ValueError:
            print(f"Entrez un nombre entier.")


def valide_iuk(query: str) -> bool:
    valid = ''
    while valid not in ['o', 'n']:
        valid = input(f"Vous avez saisie {query}, est-ce correct ? [o/n] ").lower()
    return valid == 'o'

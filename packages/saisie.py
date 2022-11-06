MAX_QUOTE_BG = 20000

def query_battletag() -> str:
    while True:
        response = input("Quel est le compte recherché : ")
        if valide_iuk(response):
            return response

def query_int_value_min_max(texte: str,min: int, max: int) -> int:
    quote_uk = -1
    while True:
        try:
            response=int(input(f"{texte} (entre {min} et {max}) : "))
            if 0 < response < MAX_QUOTE_BG and valide_iuk(response) :
                return response
            else:
                print(f"Entrez un nombre entier compris entre {min} et {max}.")

        except ValueError:
            print(f"Entrez un nombre entier.")

def valide_iuk(query:str)->str:
    valid=''
    while valid not in ['o','n']:
        valid = input(f"Vous avez saisie {query}, est-ce correct ? [o/n] ").lower()
    return valid == 'o'



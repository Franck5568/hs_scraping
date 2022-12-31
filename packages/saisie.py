from pathlib import Path
import tomllib
import tomli_w


class HsInfo:
    TOML_FILENAME = 'properties.toml'
    KEY_QUOTE_MAX = 'quote_max'
    KEY_SEASON = 'saison'
    KEY_BATTLE_TAG = 'battle_tag'
    KEY_BATTLE_QUOTE = 'user_quote'

    def __init__(self):
        self.quote_max = 20000
        self.properties = {}
        self.toml_full_filename = Path.home().joinpath(self.TOML_FILENAME)
        self.load_data()

    def load_data(self) -> None:
        # si fichier properties exists
        if Path.is_file(self.toml_full_filename):
            with open(self.toml_full_filename, 'rb') as f:
                self.properties = tomllib.load(f)
            self.quote_max = self.properties.get(HsInfo.KEY_QUOTE_MAX, 20000)
        # sinon on demande les valeurs
        else:
            self.properties[HsInfo.KEY_SEASON] = self.query_int_value_min_max(texte="Entrer une saison :", i_min=0, i_max=99)
            self.properties[HsInfo.KEY_BATTLE_QUOTE] = self.query_int_value_min_max(texte="Entrer votre quote :", i_min=0, i_max=self.quote_max)
            self.properties[HsInfo.KEY_BATTLE_TAG] = self.query_str(texte="Quel est le compte recherché :")
            # on stock la propriété quote max pour is à jour hors prog
            self.properties[HsInfo.KEY_QUOTE_MAX] = self.quote_max

            # on sauvegarde l'ensemble des propriétés
            self.save_data()

    def save_data(self) -> None:
        with open(self.toml_full_filename, 'wb') as f:
            tomli_w.dump(self.properties, f)

    @staticmethod
    def query_str(texte: str) -> str:
        while True:
            response = input(f"{texte}")
            if HsInfo.valide_iuk(response):
                return response

    @staticmethod
    def query_int_value_min_max(texte: str, i_min: int, i_max: int) -> int:
        while True:
            try:
                response = int(input(f"{texte} (entre {i_min} et {i_max}) : "))
                if i_min < response < i_max and HsInfo.valide_iuk(str(response)):
                    return response
                else:
                    print(f"Entrez un nombre entier compris entre {i_min} et {i_max}.")

            except ValueError:
                print("Entrez un nombre entier.")

    @staticmethod
    def valide_iuk(query: str) -> bool:
        valid = ''
        while valid not in ['o', 'n']:
            valid = input(f"Vous avez saisie {query}, est-ce correct ? [o/n] ").lower()
        return valid == 'o'

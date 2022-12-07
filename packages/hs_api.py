import requests
import json


class HsApi:
    # root url BG
    URL_BG_ROOT = "https://hearthstone.blizzard.com/fr-fr/api/community/leaderboardsData?region=EU&leaderboardId" \
                  "=battlegrounds"

    def __init__(self, saison: int, updated_run: str) -> None:
        # id de la saison courrante saison - 1
        self.season_id = saison - 1
        self.updated_run = updated_run
        # url root
        self.url_page_num = f'{HsApi.URL_BG_ROOT}&seasonId={self.season_id}&page='

        # info joueurs page courante
        self.current_page_players = {}
        # last page set to default value up to page_num_number
        self.bottom_page = 0
        # current_page
        self.top_page = 0
        # top rank
        self.top_quote = 0
        # bot rank
        self.bottom_quote = 0
        # max page
        self.max_page = 0

    def api_set_last_page(self, info_json: dict) -> None:
        if info_json:
            self.bottom_page = info_json['leaderboard']['pagination']['totalPages']

    def api_set_current_page_players(self, joueurs: dict, page: int) -> None:
        # init page courante
        self.current_page_players = {
            joueur['accountid']: {'page': page, 'rang': joueur['rank'], 'quote': joueur['rating'],
                                  'updated': self.updated_run} for joueur in joueurs}

    def api_get_info(self) -> dict:
        cpt: int = 1
        try:
            while True:
                response = requests.get(f'{self.url_page_num}{self.bottom_page}')
                # conversion json en dictionnaire
                response_json: dict = json.loads(response.text)
                if response_json.get('leaderboard').get('rows').__len__() > 0:
                    break
                print(f"Echec connexion, tentative de récupération n° {cpt}")
                cpt += 1
            return response_json

        except requests.exceptions.HTTPError as error:
            print(error)

    def api_get_top_page_info(self) -> dict:
        response_json = self.api_get_info()
        if not self.bottom_page:
            self.api_set_last_page(response_json)

        # memorise de la page interrogée
        self.api_set_current_page_players(joueurs=response_json['leaderboard']['rows'], page=self.top_page)
        # set current top rank
        l: list = list(self.current_page_players.values())
        self.top_quote = l[0]['quote']
        print(f'chargement de la page top : Page comprise entre {self.top_page} et {self.bottom_page}, quote est '
              f'inférieure à {self.top_quote}')
        return self.current_page_players

    def api_get_bottom_page_info(self) -> dict:
        response_json = self.api_get_info()
        # memorise de la page interrogée
        self.api_set_current_page_players(joueurs=response_json['leaderboard']['rows'], page=self.bottom_page)
        # get last element
        l: list = list(self.current_page_players.values())
        self.bottom_quote = l[-1]['quote']
        if not self.max_page:
            self.max_page = self.bottom_page
        # retourne les derniers du classement
        print(f'chargement de la page bot : Page comprise entre {self.top_page} et {self.bottom_page}, Votre quote '
              f'est supérieure à {self.bottom_quote}')
        return self.current_page_players

    # except requests.exceptions.HTTPError as error:
    #     print(error)

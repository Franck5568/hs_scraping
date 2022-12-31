import requests
import json
import time


class HsApi:
    # root url BG
    _URL_BG_ROOT = "https://hearthstone.blizzard.com/fr-fr/api/community/leaderboardsData?region=EU&leaderboardId" \
                   "=battlegrounds"

    def __init__(self, saison: int) -> None:
        # id de la saison courante saison - 1
        self._response_json = {}
        self._season_id = saison - 1
        # url root
        self.url_page_num = f'{HsApi._URL_BG_ROOT}&seasonId={self._season_id}&page='

        # info joueurs page courante
        self._current_page_players = {}
        # nombre de personnes dans la classement
        self.nbr_members = 0
        # current_page
        self.current_page = 1
        # top rank
        self.current_quote_top = 0
        # bot rank
        self.current_quote_bot = 0
        # max page
        self.max_page = 0

    def __api_set_last_page(self) -> None:
        if self._response_json:
            self.max_page = self._response_json['leaderboard']['pagination']['totalPages']

    def api_get_nbr_members(self) -> None:
        page = self.current_page
        self.current_page = self.max_page
        self.api_get_page_info()
        l: list = list(self._current_page_players.values())
        self.nbr_members = int(l[-1]['rang'])
        self.current_page = page
        self.api_get_page_info()

    def __api_set_current_page_players(self, players_in_current_page: dict) -> None:
        # init page courante
        self._current_page_players = {
            joueur['accountid']: {'page': self.current_page, 'rang': joueur['rank'], 'quote': joueur['rating']}
            for joueur in players_in_current_page}
        # update max page
        self.__api_set_last_page()

    def __api_get_rest_hs(self) -> dict:
        cpt: int = 1
        try:
            while True:
                response = requests.get(f'{self.url_page_num}{self.current_page}')
                # conversion json en dictionnaire
                response_json: dict = json.loads(response.text)
                if response_json.get('leaderboard').get('rows').__len__() > 0:
                    break
                print(f"Echec connexion, tentative de récupération n° {cpt}")
                cpt += 1
                time.sleep(cpt)
            return response_json

        except requests.exceptions.HTTPError as error:
            print(error)

    def api_get_page_info(self) -> None:
        self._response_json = self.__api_get_rest_hs()

        # memorise de la page interrogée
        self.__api_set_current_page_players(players_in_current_page=self._response_json['leaderboard']['rows'])
        # update keys in lower
        self.set_lowercase_key()
        # update current quotes
        l: list = list(self._current_page_players.values())
        self.current_quote_top = l[0]['quote']
        self.current_quote_bot = l[-1]['quote']
        print(f'chargement de la page {self.current_page} : Quotes comprises entre {self.current_quote_bot} et '
              f'{self.current_quote_top}')

    def find_tag(self, tag: str) -> int:
        if self._current_page_players.get(tag, ''):
            return self._current_page_players.get(tag).get('rang', -1)
        else:
            return -1

    def set_lowercase_key(self):
        keys: list = list(self._current_page_players.keys())
        for k in keys:
            self._current_page_players[str(k).lower()] = self._current_page_players.pop(k)

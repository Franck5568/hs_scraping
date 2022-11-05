from urllib import response
import requests
import json


class hsApi:
    # root url BG
    URL_BG_ROOT="https://hearthstone.blizzard.com/fr-fr/api/community/leaderboardsData?region=EU&leaderboardId=battlegrounds"
    # id de la saison courrante saison - 1
    SEASON_ID=7

    def __init__(self ) -> None:
        # hall of fame list
        self.hall_of_fame=[]
        # page to resquest
        self.page_number=1
        # last page set to default value up to page_num_number
        self.last_page=0
        # url root
        self.url_page_num=f'{hsApi.URL_BG_ROOT}&seasonId={hsApi.SEASON_ID}&page='
        # current_page
        self.current_page = 0
        # first page with rank player
        self.first_page_rank_player = 0

    def set_last_page(self, info_json:dict) -> None:
        if info_json:
            self.last_page = info_json['leaderboard']['pagination']['totalPages']

    def get_page_info(self, page: int) -> None:
        # appel web
        response = requests.get(f'{self.url_page_num}{page}')
        # conversion json en dictionnaire
        response_json = json.loads(response.text)
        # dernière page si non définie
        if not self.last_page:
            self.set_last_page(response_json)
        # memorise de la page interrogée
        self.current_page_players = response_json['leaderboard']['rows']
        # enregistrement des 25 premiers
        self.hall_of_fame.extend(self.current_page_players)

    def get_min_rank_in_page(self) -> None:
        pass

    def find_tagname_in_page(self) -> None:
        pass

    def get_first_page_with_rank_player(self) -> None:
        pass
from urllib import response
import requests
import json


class hsApi:
    # root url BG
    URL_BG_ROOT="https://hearthstone.blizzard.com/fr-fr/api/community/leaderboardsData?region=EU&leaderboardId=battlegrounds"

    def __init__(self, saison:int) -> None:
        # id de la saison courrante saison - 1
        self.season_id = saison - 1
        # url root
        self.url_page_num=f'{hsApi.URL_BG_ROOT}&seasonId={self.season_id}&page='

        #### init variables for later
        # info joueurs page courante
        self.current_page_players = {}
        # last page set to default value up to page_num_number
        self.last_page=0
        # current_page
        self.current_page = 0
 
    def api_set_last_page(self, info_json:dict) -> None:
        if info_json:
            self.last_page = info_json['leaderboard']['pagination']['totalPages']

    def api_set_current_page_players(self, joueurs: dict) -> None:
        # init page courrante
        self.current_page_players={}

        for joueur in joueurs:
            self.current_page_players[joueur['accountid']] = {'page':self.current_page ,
                                                    'rang':joueur['rank'], 
                                                    'quote':joueur['rating']}

    def api_get_page_info(self) -> dict:
        # appel web
        response = requests.get(f'{self.url_page_num}{self.current_page}')
        # conversion json en dictionnaire
        response_json = json.loads(response.text)
        # dernière page si non définie
        if not self.last_page:
            self.api_set_last_page(response_json)
        # memorise de la page interrogée
        self.api_set_current_page_players(joueurs=response_json['leaderboard']['rows']) 
        return self.current_page_players
    
    def api_get_min_rank_in_page(self) -> None:
        pass

    def api_find_tagname_in_page(self) -> None:
        pass

    def api_get_first_page_with_rank_player(self, bg_tag:str, bg_quote:int) -> None:
        pass
 

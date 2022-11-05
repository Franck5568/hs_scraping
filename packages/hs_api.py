from urllib import response
import packages.player_info as player
import requests
import json


class hsApi:
    # root url BG
    URL_BG_ROOT="https://hearthstone.blizzard.com/fr-fr/api/community/leaderboardsData?region=EU&leaderboardId=battlegrounds"
    # id de la saison courrante saison - 1
    SEASON_ID=7

    def __init__(self ) -> None:
        # hall of fame dictionnaire
        self.hall_of_fame={}
        # info joueurs page courante
        self.current_page_players={}
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

    def api_set_last_page(self, info_json:dict) -> None:
        if info_json:
            self.last_page = info_json['leaderboard']['pagination']['totalPages']

    def api_set_current_page_players(self, joueurs: dict) -> None:
        p: player.playerInfo
        # init page courrante
        self.current_page_players={}

        for joueur in joueurs:
            p = player.playerInfo(page=self.current_page ,rang=joueur['rank'], bg_tag=joueur['accountid'],quote=joueur['rating'])
            self.current_page_players[p.account] = p.get_player_info()

    def api_get_page_info(self) -> None:
        # appel web
        response = requests.get(f'{self.url_page_num}{self.current_page}')
        # conversion json en dictionnaire
        response_json = json.loads(response.text)
        # dernière page si non définie
        if not self.last_page:
            self.api_set_last_page(response_json)
        # memorise de la page interrogée
        self.api_set_current_page_players(joueurs=response_json['leaderboard']['rows'])
        # enregistrement des 25 premiers
        self.hall_of_fame.update(self.current_page_players)  
    
    def api_get_min_rank_in_page(self) -> None:
        pass

    def api_find_tagname_in_page(self) -> None:
        pass

    def api_get_first_page_with_rank_player(self, bg_tag:str, bg_quote:int) -> None:
        pass
        # check if bg_tag is in memory (or json later)

        # if found check get bg_quote == quote in memory
        #   if == end
        #   if lesser check api page + 1 until found
        #   if greater check api page page - 1 until found
        # update memory (json later)

        # if not found : find memory_quote nearest to get the page to begin query
        # if gap between user quote and memory quote greater than 10% (dynamically later)
        #   if gap greater than 10% get current_page = (last_page - current_page) / 2 and get_info
        #   elif user_quote > memory_quote : current_page -= 1
        #   else (user_quote < memory_quote) : current_page += 1


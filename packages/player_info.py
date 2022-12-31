from pathlib import Path
import datetime
import json


class PlayerInfo:
    JSON_FILENAME = '.halloffame.json'

    def __init__(self, tagname: str, userquote: int) -> None:
        # set init minute of update launch
        self.updated_minute = self.set_updated_time()
        self.hall_of_fame = {}
        self.tagname = tagname
        self.userquote = userquote
        self.last_good_page_top = 0
        self.last_good_page_bot = 0
        self.save_filename = Path.home().joinpath(self.JSON_FILENAME)

    def update(self, players_25_api: dict) -> None:
        self.hall_of_fame.update(players_25_api)

    def find_bg_tagname(self) -> int:
        """
        return 1 : si tagname en mémoire et updated date est la date du jour
        return 0 : si tagname en mémoire mais non à jour
        return -1: si tagname not found 
        """
        check_memory: str = self.hall_of_fame.get(self.tagname, '')
        if not check_memory:
            # donnée n'est pas en mémoire
            return -1
        if self.hall_of_fame.get(self.tagname).get('updated') == self.updated_minute:
            # rien à faire tout est à jour on a trouvé
            return 1
        else:
            # on doit mettre à jour la donnée en mémoire
            return 0

    def get_ranking(self) -> int:
        return self.hall_of_fame.get(self.tagname).get('rang')

    def get_page(self) -> int:
        return self.hall_of_fame.get(self.tagname).get('page')

    @staticmethod
    def set_updated_time():
        # updated minute
        updated_minute: str = str(datetime.datetime.now())
        return updated_minute[:updated_minute.rfind(':')]

    def get_page_quote_max(self, page: int) -> int:
        return max(v['quote'] for v in self.hall_of_fame.values() if v['page'] == page)

    def get_page_quote_min(self, page: int) -> int:
        return min(v['quote'] for v in self.hall_of_fame.values() if v['page'] == page)

    def del_player_info(self) -> None:
        self.hall_of_fame.pop(self.tagname)

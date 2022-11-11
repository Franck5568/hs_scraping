import os
from pathlib import Path
import datetime
import json


class PlayerInfo:
    JSON_FILENAME = '.halloffame.json'

    def __init__(self, tagname: str, userquote: int) -> None:
        self.hall_of_fame = {}
        self.tagname = tagname
        self.userquote = userquote
        self.last_good_page_top = 0
        self.last_good_page_bot = 0
        self.save_filename = os.path.join(Path.home(), self.JSON_FILENAME)

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
        if self.hall_of_fame.get(self.tagname).get('updated') == str(datetime.date.today()):
            # rien à faire tout est à jour on a trouvé
            return 1
        else:
            # on doit mettre à jour la donnée en mémoire
            return 0

    def get_ranking(self) -> int:
        return self.hall_of_fame.get(self.tagname).get('rang')

    def get_page(self) -> int:
        return self.hall_of_fame.get(self.tagname).get('page')

    def get_page_quote(self, page: int) -> int:
        return max([(v['quote']) for v in self.hall_of_fame.values() if v['page'] == page])

    #    def get_player_info(self) -> dict:
    #        return {'rank':self.rank,'rating':self.rating,'page':self.page}

    def load_json(self) -> dict:
        if os.path.exists(self.save_filename):
            with open(self.save_filename, 'r') as f:
                return json.load(f)
        else:
            return {}

    def save_json(self) -> None:
        with open(self.save_filename, 'w') as f:
            json.dump(self.hall_of_fame, f, indent=4)

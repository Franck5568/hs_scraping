import os
from pathlib import Path

class playerInfo:
    
    JSON_FILENAME ='.halloffame.json'

    def __init__(self) -> None:
        self.hall_of_fame = {}

    def update(self, players_25_api :dict) -> None:
        self.hall_of_fame.update(players_25_api)

    def get_quote_of_tag(self, tag_name:str) -> int:
        self.hall_of_fame.get(tag_name, '')
        print('test')
        return 5

    def get_player_info(self) -> dict:
        return {'rank':self.rank,'rating':self.rating,'page':self.page}

    @classmethod
    def load_json(cls) -> dict:
        cls.save_filename = os.path.join(Path.home(),cls.JSON_FILENAME)
        if os.path.exists(cls.save_filename):
            print('exist')
        else:
            return {}

    @classmethod
    def save_json(cls) -> None:
        pass

if __name__ == '__main__':
    playerInfo.load_json()
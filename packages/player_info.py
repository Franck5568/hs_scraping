import os
from pathlib import Path

class playerInfo:
    
    JSON_FILENAME ='.halloffame.json'

    def get_player_info(self) -> dict:
        return {'rank':self.rank,'rating':self.rating,'page':self.page}

    @classmethod
    def load_json(cls) -> dict:
        cls.savefile = os.path.join(Path.home(),cls.JSON_FILENAME)
        if os.path.exists(cls.savefile):
            print('exist')
        else:
            return {}

if __name__ == '__main__':
    playerInfo.load_json()
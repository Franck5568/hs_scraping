class playerInfo:
    def __init__(self, rang:int, bg_tag:str, quote:int) -> None:
        self.rank = rang
        self.account = bg_tag
        self.rating = quote

    def get_player_info(self) -> dict:
        return {'rank':self.rank,'rating':self.rating}
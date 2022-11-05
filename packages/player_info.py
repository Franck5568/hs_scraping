class playerInfo:
    def __init__(self, page: int, rang:int, bg_tag:str, quote:int) -> None:
        self.rank = rang
        self.account = bg_tag
        self.rating = quote
        self.page = page

    def get_player_info(self) -> dict:
        return {'rank':self.rank,'rating':self.rating,'page':self.page}
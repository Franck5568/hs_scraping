import packages.saisie as iuk
import packages.hs_api as hs


# Input query quotation
# bg_tag = iuk.query_battletag()
bg_tag = 'sinquem'
#input username
# bg_quote = iuk.query_quote()
bg_quote = 6000

hof = hs.hsApi()
# chargement de la page 1 et de la dernière page
hof.current_page=1
hof.api_get_page_info()

hof.api_get_first_page_with_rank_player(bg_tag=bg_tag, bg_quote=bg_quote)
# recherche page du rang
print(hof.last_page)


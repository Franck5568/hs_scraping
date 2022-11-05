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
hof.get_page_info(1)

hof.get_first_page_with_rank_player()
# recherche page du rang
print(hof.last_page)


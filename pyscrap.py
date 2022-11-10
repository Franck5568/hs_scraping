import packages.saisie as iuk
import packages.hs_api as hs
import packages.player_info as player


# Input query quotation
# bg_tag = iuk.query_battletag()
bg_tag = 'sinquem'
#input username
# bg_quote = iuk.query_int_value_min_max(texte="Entrer votre quote :", min=0, max=20000)
bg_quote = 6367
#input saison
# bg_saison = iuk.query_int_value_min_max(texte="Entrer une saison :", min=0, max=8)
bg_saison = 8

# load json from disque
hof_histo = player.playerInfo()

# objet for rest queries
hof_api = hs.hsApi(saison=8)

# not save file
if not hof_histo.hall_of_fame:
    # chargement de la page 1 et de la dernière page
    hof_api.current_page=1
    # update du des données chargées
    hof_histo.update(hof_api.api_get_page_info())

# check if bg_tag is in memory
print(hof_histo.get_quote_of_tag(tag_name=bg_tag))
# if found check get bg_quote == quote in memory
#   if == end data in memory
#   if lesser check api page + 1 until found
#   if greater check api page page - 1 until found
# update memory (json later)

# if not found : find memory_quote nearest to get the page to begin query
# if gap between user quote and memory quote greater than 10% (dynamically later)
#   if gap greater than 10% get current_page = (last_page - current_page) / 2 and get_info
#   elif user_quote > memory_quote : current_page -= 1
#   else (user_quote < memory_quote) : current_page += 1

# recherche page du rang
print(hof_api.last_page)

import packages.saisie as iuk
import packages.hs_api as hs
import packages.player_info as player
import math

props = iuk.HsInfo()

# objet for rest queries
hof_api = hs.HsApi(saison=props.properties[props.KEY_SEASON])

# chargement de la page 1
hof_api.top_page = 1
# update du des données chargées
hof_histo.update(hof_api.api_get_top_page_info())

# init before run
tag_in_current_page: int = 0

# memo last good top and bot
hof_histo.last_good_page_top = hof_api.top_page
hof_histo.last_good_page_bot = hof_api.bottom_page

# get the bigger power 2 nearest page number
page_step: int = 2**int(math.log2(hof_api.max_page))

while tag_in_current_page < 1:
    # check if bg_tag is in memory
    tag_in_current_page: int = hof_histo.find_bg_tagname()

    ## la page courante de recherche est en mémoire
    if tag_in_current_page == 0:    
        hof_api.bottom_page = hof_histo.get_page()
        # il faut supprimer la donner en mémoire
        hof_histo.del_player_info()
        # on recharge la page mémorisé depuis le web
        # hof_histo.update(hof_api.api_get_bottom_page_info())

    ## trouvé on affiche et on sort
    elif tag_in_current_page == 1:
        print(f"Vous êtes classé : {hof_histo.get_ranking()}")

    ## ni en mémoire ni trouvé sur le web
    # la quote est entre le top et le bot
    elif hof_api.top_quote > hof_histo.userquote >= hof_api.bottom_quote:
        # On mémorise les bornes actuelles
        hof_histo.last_good_page_bot = hof_api.bottom_page
        hof_histo.last_good_page_top = hof_api.top_page

        # manage page_step
        if hof_histo.userquote - hof_api.bottom_quote <= 1:
            page_step = 1
        else:
            # page_step managment
#            while hof_api.bottom_page < page_step:
            page_step = max(page_step // 2, 1)

        # change page
        hof_api.bottom_page -= page_step

        # on charge les pages en mémoire
#        hof_histo.update(hof_api.api_get_bottom_page_info())

    # On a remonté le bas trop haut
    elif hof_api.bottom_quote > hof_histo.userquote:
        if hof_api.bottom_quote > 0:
            # on depasse on divise par 2 le pas, jamais moins de 1
            page_step = max(page_step // 2, 1)
            # le top devient le bot
            hof_api.top_page = hof_api.bottom_page
            # api reprend la dernière bonne bot page en mémoire
            hof_api.bottom_page = hof_histo.last_good_page_bot
            # mémorise le dernier top ok
            hof_histo.last_good_page_top = hof_api.top_page
            # reload page in memory
 #           hof_api.top_quote = hof_histo.get_page_quote_max(page=hof_histo.last_good_page_top)
 #           hof_api.bottom_quote = hof_histo.get_page_quote_min(page=hof_histo.last_good_page_bot)
        else:
            print(f"Pseudo {hof_histo.tagname} non trouvé en ligne ou quote à Zéro.")
            break
    # on a descendu le top trop bas
    elif hof_api.top_quote < hof_histo.userquote:
        page_step = max(page_step // 2, 1)
        # le bot devient le top
        hof_api.bottom_page = hof_api.top_page
        # api reprend la dernière bonne top page en mémoire
        hof_api.top_page = hof_histo.last_good_page_bot
        # mémorise le dernier bot ok
        hof_histo.last_good_page_bot = hof_api.bottom_page
    else:
        print(f"Pseudo {hof_histo.tagname} non trouvé en ligne ou quote mauvaise.")
        break
    hof_histo.update(hof_api.api_get_bottom_page_info())
    hof_histo.update(hof_api.api_get_top_page_info())
# sauvegarde de la mémoire
hof_histo.save_json()

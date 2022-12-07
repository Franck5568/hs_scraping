import packages.saisie as iuk
import packages.hs_api as hs
import packages.player_info as player
import math

bg_tag = iuk.query_battletag()

bg_quote = iuk.query_int_value_min_max(texte="Entrer votre quote :", imin=0, imax=20000)

# input saison
# bg_saison = iuk.query_int_value_min_max(texte="Entrer une saison :", min=0, max=8)
bg_saison = 8

# load json from disque
hof_histo = player.PlayerInfo(tagname=bg_tag, userquote=bg_quote)
hof_histo.load_json()

# objet for rest queries
hof_api = hs.HsApi(saison=bg_saison, updated_run=hof_histo.updated_minute)

# que le fichier soit présents ou pas on charge la 1ere et la derniere page du web en mémoire
# chargement de la page 1
hof_api.top_page = 1
# update du des données chargées
hof_histo.update(hof_api.api_get_top_page_info())
# load last page et la dernière place
hof_histo.update(hof_api.api_get_bottom_page_info())

# init before run
tag_in_current_page: int = 0

# memo last good
hof_histo.last_good_page_top = hof_api.top_page
hof_histo.last_good_page_bot = hof_api.bottom_page

# get the bigger power 2 nearest page number
page_step: int = 2**int(math.log2(hof_api.max_page))

while tag_in_current_page < 1:
    # check if bg_tag is in memory
    tag_in_current_page: int = hof_histo.find_bg_tagname()
    if tag_in_current_page == 0:
        # la page courante de recherche est en mémoire
        hof_api.bottom_page = hof_histo.get_page()
        # il faut supprimer la donner en mémoire
        hof_histo.del_player_info()

        # on recharge la page mémorisé depuis le web
        hof_histo.update(hof_api.api_get_bottom_page_info())

    elif tag_in_current_page == 1:
        print(f"Vous êtes classé : {hof_histo.get_ranking()}")

    elif hof_api.top_quote > hof_histo.userquote >= hof_api.bottom_quote:
        # la quote est entre le top et le bot
        # On mémorise le bas actuel
        hof_histo.last_good_page_bot = hof_api.bottom_page

        # manage page_step
        if hof_histo.userquote - hof_api.bottom_quote <= 1:
            page_step = 1
        else:
            # page_step managment
            while hof_api.bottom_page < page_step:
                page_step = max(page_step // 2, 1)

        # change page
        hof_api.bottom_page -= page_step

        # on charge les pages en mémoire
        hof_histo.update(hof_api.api_get_bottom_page_info())

    elif hof_api.bottom_quote > hof_histo.userquote:
        # plancher trop haut
        if hof_api.bottom_quote > 0:
            # on depasse on divise par 2 le pas, jamais moins de 1
            page_step = max(page_step // 2, 1)
            # le top devient le bot
            hof_api.top_page = hof_api.bottom_page
            # api repprend la dernière bonne bot page en mémoire
            hof_api.bottom_page = hof_histo.last_good_page_bot

            # mémorise le dernier top ok
            hof_histo.last_good_page_top = hof_api.top_page
            # reload page in memory
            hof_api.top_quote = hof_histo.get_page_quote_max(page=hof_histo.last_good_page_top)
            hof_api.bottom_quote = hof_histo.get_page_quote_min(page=hof_histo.last_good_page_bot)
        else:
            print(f"Pseudo {hof_histo.tagname} non trouvé en ligne ou quote à Zéro.")
            break
    else:
        print(f"Pseudo {hof_histo.tagname} non trouvé en ligne ou quote mauvaise.")
        break

# sauvegarde de la mémoire
hof_histo.save_json()

import packages.saisie as iuk
import packages.hs_api as hs
import packages.player_info as player

# bg_tag = iuk.query_battletag()
bg_tag = 'sinquem'

# bg_quote = iuk.query_int_value_min_max(texte="Entrer votre quote :", min=0, max=20000)
bg_quote = 6270

# input saison
# bg_saison = iuk.query_int_value_min_max(texte="Entrer une saison :", min=0, max=8)
bg_saison = 8

# load json from disque
hof_histo = player.PlayerInfo(tagname=bg_tag, userquote=bg_quote)
hof_histo.load_json()

# objet for rest queries
hof_api = hs.HsApi(saison=8)

# que le fichier soit préent ou pas on charge la 1ere et la derniere page du web en mémoire
# chargement de la page 1 et de la dernière page
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
page_par_page: int = False
page_step: int = 2048
while tag_in_current_page < 1:
    # check if bg_tag is in memory
    tag_in_current_page: int = hof_histo.find_bg_tagname()
    if tag_in_current_page == 1:
        print(f"Vous êtes classé : {hof_histo.get_ranking()}")

    # on ajoute des pages en ligne dans la mémoire pour rechercher
    elif tag_in_current_page == 0:
        # la page courante de recherche est celle en mémoire
        hof_api.bottom_page = hof_histo.get_page()

        # on charge la page en mémoire
        hof_histo.update(hof_api.api_get_bottom_page_info())

    else:
        # tag non trouvé on recherche par dichotomie

        if hof_api.top_quote > hof_histo.userquote >= hof_api.bottom_quote:
            # la quote est entre le top et le bot
            # le plancher est remonté de la moitié de l'écart
            hof_histo.last_good_page_bot = hof_api.bottom_page
            # nous sommes dans les pages de la quote (il se peux que ce soit une page déjà passée !)
            if hof_histo.userquote - hof_api.bottom_quote <= 1:
                page_step = 1

            if page_par_page:
                hof_api.bottom_page -= page_step
            else:
                hof_api.bottom_page //= 2

            # on charge les pages en mémoire
            hof_histo.update(hof_api.api_get_bottom_page_info())

        elif hof_api.bottom_quote > hof_histo.userquote:
            # plancher trop haut
            if hof_api.bottom_quote > 0:
                page_par_page = True
                # on depasse on divise par 2 le pas, jamais moins de 1
                page_step = max(page_step // 2, 1)
                # le top devient le bot
                hof_api.top_page = hof_api.bottom_page
                # nouvelle ref top page
                hof_histo.last_good_page_top = hof_api.top_page
                # api repprend la dernière bonne bot page en mémoire
                hof_api.bottom_page = hof_histo.last_good_page_bot
                # reload page in memory
                hof_api.top_quote = hof_histo.get_page_quote(page=hof_histo.last_good_page_top)
                hof_api.bottom_quote = hof_histo.get_page_quote(page=hof_histo.last_good_page_bot)
            else:
                print(f"Pseudo {hof_histo.tagname} non trouvé en ligne ou quote à Zéro.")
                break

# sauvegarde de la mémoire
hof_histo.save_json()

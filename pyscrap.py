import packages.saisie as info
import packages.hs_api as hs
import packages.player_info as player
import math

# load properties
props: info.HsInfo = info.HsInfo()

# variable qj contient la quote du joueur +1 pour
qj: int = props.properties[props.KEY_BATTLE_QUOTE] + 1
battle_tag: str = props.properties[props.KEY_BATTLE_TAG]

# objet for rest queries
hs_api: hs.HsApi = hs.HsApi(saison=props.properties[props.KEY_SEASON])

# lecture page 1
hs_api.api_get_page_info()

# recherche du nombre de membres
hs_api.api_get_nbr_members()

# get the bigger power 2 nearest page number
page_step: int = 2 ** int(math.log2(hs_api.max_page))

while True:
    # quote du joueur supérieur quote top de la page actuelle
    if qj > hs_api.current_quote_top:
        # on recule de step_page // 2
        page_step = max(page_step // 2, 1)
        hs_api.current_page -= page_step
    # quote du joueur inférieur quote bas de page actuelle
    elif qj < hs_api.current_quote_bot:
        # on avance de step pages
        hs_api.current_page += page_step
    # sinon c'est soit = top ou bot = quote recherchée + 1
    # premier cas la quote_top == qj (tjs +1)
    elif hs_api.current_quote_top == qj:
        page_step = 1
        # on recherche jusqu'à ce que qj-1 < bot
        while hs_api.current_quote_bot > qj-1:
            hs_api.current_page += page_step
            hs_api.api_get_page_info()
            # recherche pseudo
            pos: int = hs_api.find_tag(battle_tag.lower())
            if pos >= 0:
                print(f'Pseudo {battle_tag} trouvé avec la quote {qj-1} en position {pos} sur {hs_api.nbr_members}')
                break
        print(f'pseudo {battle_tag} non trouvé avec une quote de {qj-1}')
        break
    elif hs_api.current_quote_bot == qj:
        page_step = 1
        # on recherche jusqu'à ce que qj-1 > top
        while hs_api.current_quote_top < qj-1:
            hs_api.current_page -= page_step
            hs_api.api_get_page_info()
            # recherche pseudo
            pos: int = hs_api.find_tag(battle_tag.lower())
            if pos >= 0:
                print(f'Pseudo {battle_tag} trouvé avec la quote {qj-1} en position {pos} sur {hs_api.nbr_members}')
                break
        print(f'pseudo {battle_tag} non trouvé avec une quote de {qj - 1}')
        break

    hs_api.api_get_page_info()

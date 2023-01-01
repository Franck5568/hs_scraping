import packages.saisie as info
import packages.hs_api as hs
import math

# load properties
props: info.HsInfo = info.HsInfo()

# variable qj contient la quote du joueur +1 pour
qj: int = props.properties[props.KEY_BATTLE_QUOTE]
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
    if qj+1 > hs_api.current_quote_top:
        # on recule de step_page // 2
        page_step = max(page_step // 2, 1)
        hs_api.current_page -= page_step
    elif qj < hs_api.current_quote_bot:
        # on avance de step pages
        hs_api.current_page += page_step
    else:
        page_step = 1

        while qj in [hs_api.current_quote_top + 1, hs_api.current_quote_top, hs_api.current_quote_bot]:
            hs_api.current_page += page_step
            hs_api.api_get_page_info()
            # contrôle de la presence du battle tag dans la page
            pos: int = hs_api.find_tag(battle_tag.lower())
            if pos >= 0:
                print(f'Pseudo {battle_tag} trouvé avec la quote {qj} en position {pos} sur {hs_api.nbr_members}')
                break

    if page_step == 1:
        print(f'pseudo {battle_tag} non trouvé avec une quote de {qj}')
        break

    hs_api.api_get_page_info()

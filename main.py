import pandas as pd
import json

import module.fournisseur as _frnssr

if __name__ == "__main__":

    # Récupération des données de configuration
    with open('data/config.json') as config_file:
        config = json.load(config_file)
        famille_article = config['famille_article']

    # Récupération du dictionnaire de référence fournisseur
    new_ref = False
    ref_fournisseur = _frnssr.dict_reference('rexel')

    # Récupération des données utilisées du fichier d'export
    data, intitules = _frnssr.read_data(config, 'rexel')

    # Ajout des nouvelles colonnes
    vide  = pd.Series([''] * len(data))
    ach_col = pd.Series(['ACH'] * len(data))

    #######################

    familles_input = list()

    for i in range(len(data)):
        if data[intitules[2]][i] in ref_fournisseur:
            input_temp = ref_fournisseur[data[intitules[2]][i]]
        else:
            input_temp = input('Famille pour l\'article ' + data[intitules[2]][i] + ' - ' + data[intitules[1]][i] + ': ')
            ref_fournisseur[data[intitules[2]][i]] = input_temp

            # Si détection de la première nouvelle référence
            if not new_ref:
                for i in range(len(famille_article)):
                    print(i+1, '-', famille_article[i])

                new_ref = True
        try:
            familles_input.append(famille_article[int(input_temp)-1])
        except:
            familles_input.append('')

    famile_col = pd.Series(familles_input)

    #######################

    concat_col = data[intitules[2]] + ' - ' + data[intitules[1]]

    data.insert(len(data.columns), 'VIDE_1', vide)
    data.insert(len(data.columns), 'VIDE_2', vide)
    data.insert(len(data.columns), 'ACH', ach_col)
    data.insert(len(data.columns), 'FAMILLE', famile_col)
    data.insert(len(data.columns), 'EXEMPLE', concat_col)

    # Réorganisation des colonnes
    data = data[[intitules[2], intitules[1], 'VIDE_1', intitules[0], intitules[3], 'VIDE_2', 'ACH', 'FAMILLE', 'EXEMPLE']]

    #Export des données en CSV
    print(data)

    data.to_csv('result/espace_affaire.csv', index=False, header=False, sep=';')

    # Sauvegarde des nouvelles références fournisseur
    if new_ref:
        _frnssr.save_ref(config, 'rexel', ref_fournisseur)

    print('Fichier exporté avec succès !')
    input('')

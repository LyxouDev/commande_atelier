import pandas as pd
import json

import module.fournisseur as _frnssr

if __name__ == "__main__":

    # Récupération des données de configuration
    with open('data/config.json') as config_file:
        config = json.load(config_file)
        famille_article = config['famille_article']

    # Sélection du fournisseur
    selection_ok = False
    while not selection_ok:
        i = 0
        list_fournisseur, list_extension = list(), list()
        for key, val in config['fournisseur'].items():
            print(i+1, '-', val['nom'])
            list_fournisseur.append(key)
            list_extension.append(val['extension'])
            i += 1

        choix = input('Sélectionner le fournisseur: ')
        try:
            choix = int(choix)
            if choix > 0 and choix <= i:
                selection_ok = True
                nom_fournisseur = list_fournisseur[choix-1]
                extension= list_extension[choix-1]
        except:
            pass

    # Récupération du dictionnaire de référence fournisseur
    new_ref = False
    ref_fournisseur = _frnssr.dict_reference(nom_fournisseur)

    # Récupération des données utilisées du fichier d'export
    data, intitules = _frnssr.read_data(config, nom_fournisseur, extension)

    # Ajout des nouvelles colonnes
    vide  = pd.Series([''] * len(data))
    ach_col = pd.Series(['ACH'] * len(data))

    #######################

    familles_input = list()

    for i in range(len(data)):
        if str(data[intitules[2]][i]) in ref_fournisseur:
            input_temp = ref_fournisseur[str(data[intitules[2]][i])]
        else:
            # Si détection de la première nouvelle référence
            if not new_ref:
                for j in range(len(famille_article)):
                    print(j+1, '-', famille_article[j])

                new_ref = True

            input_temp = input('Famille pour l\'article ' + str(data[intitules[2]][i]) + ' - ' + str(data[intitules[1]][i]) + ': ')
            ref_fournisseur[str(data[intitules[2]][i])] = input_temp
        try:
            familles_input.append(famille_article[int(input_temp)-1])
        except:
            familles_input.append('')

    famile_col = pd.Series(familles_input)

    #######################

    concat_col = data[intitules[2]].apply(str) + ' - ' + data[intitules[1]].apply(str)

    data.insert(len(data.columns), 'VIDE_1', vide)
    data.insert(len(data.columns), 'VIDE_2', vide)
    data.insert(len(data.columns), 'ACH', ach_col)
    data.insert(len(data.columns), 'FAMILLE', famile_col)
    data.insert(len(data.columns), 'EXEMPLE', concat_col)

    # Réorganisation des colonnes
    data = data[[intitules[2], intitules[1], 'VIDE_1', intitules[0], intitules[3], 'VIDE_2', 'ACH', 'FAMILLE', 'EXEMPLE']]

    #Export des données en CSV
    print(data)

    data.to_csv('export/espace_affaire.csv', index=False, header=False, sep=';', encoding='utf-8-sig')

    # Sauvegarde des nouvelles références fournisseur
    if new_ref:
        _frnssr.save_ref(nom_fournisseur, ref_fournisseur)

    print('Fichier exporté avec succès !')
    input('')

import pandas as pd
import json

if __name__ == "__main__":

    # Récupération des données de configuration
    with open('data/config.json') as config_file:
        config = json.load(config_file)

    famille_article = config['famille_article']
    usecols = ",".join([key for key, val in config['fournisseur']["rexel"]["colonne"].items()])

    # Récupération du dictionnaire de référence fournisseur
    new_ref = False
    with open('data/ref_rexel.json') as ref_file:
        ref_fournisseur = json.load(ref_file)

    # Récupération des données utilisées du fichier d'export
    data = pd.read_excel('export/export.xlsx', usecols=usecols)

    # Ajout des nouvelles colonnes
    vide  = pd.Series([''] * len(data))
    ach_col = pd.Series(['ACH'] * len(data))

    #######################

    familles_input = list()

    for i in range(len(famille_article)):
        print(i+1, '-', famille_article[i])

    for i in range(len(data)):
        if data['Réf Fab'][i] in ref_fournisseur:
            input_temp = ref_fournisseur[data['Réf Fab'][i]]
        else:
            input_temp = input('Famille pour l\'article ' + data['Réf Fab'][i] + ' - ' + data['Description du produit'][i] + ': ')
            ref_fournisseur[data['Réf Fab'][i]] = input_temp
            new_ref = True
        try:
            familles_input.append(famille_article[int(input_temp)-1])
        except:
            familles_input.append('')

    famile_col = pd.Series(familles_input)

    #######################

    concat_col = data['Réf Fab'] + ' - ' + data['Description du produit']

    data.insert(len(data.columns), 'VIDE_1', vide)
    data.insert(len(data.columns), 'VIDE_2', vide)
    data.insert(len(data.columns), 'ACH', ach_col)
    data.insert(len(data.columns), 'FAMILLE', famile_col)
    data.insert(len(data.columns), 'EXEMPLE', concat_col)

    # Réorganisation des colonnes
    data = data[['Réf Fab', 'Description du produit', 'VIDE_1', 'Quantité', 'Prix net HT', 'VIDE_2', 'ACH', 'FAMILLE', 'EXEMPLE']]

    #Export des données en CSV
    print(data)

    data.to_csv('result/espace_affaire.csv', index=False, header=False, sep=';')

    # Sauvegarde des nouvelles références fournisseur
    if new_ref:
        with open('data/ref_rexel.json', 'w') as ref_file:
            json.dump(ref_fournisseur, ref_file)

    print('Fichier exporté avec succès !')
    input('')

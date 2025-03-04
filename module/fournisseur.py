import pandas as pd
import json


def used_colonnes(config_file, nom_fournisseur):
    colonnes = list()
    intitules = list()

    colonnes.append(config_file['fournisseur'][nom_fournisseur]["informations"]['quantite']['colonne'])
    colonnes.append(config_file['fournisseur'][nom_fournisseur]["informations"]['description']['colonne'])
    colonnes.append(config_file['fournisseur'][nom_fournisseur]["informations"]['ref_fab']['colonne'])
    colonnes.append(config_file['fournisseur'][nom_fournisseur]["informations"]['prix']['colonne'])
    
    intitules.append(config_file['fournisseur'][nom_fournisseur]["informations"]['quantite']['valeur'])
    intitules.append(config_file['fournisseur'][nom_fournisseur]["informations"]['description']['valeur'])
    intitules.append(config_file['fournisseur'][nom_fournisseur]["informations"]['ref_fab']['valeur'])
    intitules.append(config_file['fournisseur'][nom_fournisseur]["informations"]['prix']['valeur'])

    return ','.join(colonnes), intitules

def dict_reference(nom_fournisseur):
    with open('data/ref_' + nom_fournisseur + '.json') as ref_file:
        return json.load(ref_file)

def read_data(config_file, nom_fournisseur, extension):
    useColonnes, intituleColonnes = used_colonnes(config_file, nom_fournisseur)
    
    if extension == 'csv':
        csv_file = pd.read_csv('export/fichier_export/export_' + nom_fournisseur + '.csv', encoding='latin1', sep=';')
        excel_file = pd.ExcelWriter('export/fichier_export/temp/export_' + nom_fournisseur + '.xlsx')
        csv_file.to_excel(excel_file, index=True)
        excel_file._save()
        return pd.read_excel('export/fichier_export/temp/export_' + nom_fournisseur + '.xlsx', usecols=useColonnes), intituleColonnes

    return pd.read_excel('export/fichier_export/export_' + nom_fournisseur + '.xlsx', usecols=useColonnes), intituleColonnes

def save_ref(nom_fournisseur, ref_fournisseur):
    with open('data/ref_' + nom_fournisseur + '.json', 'w') as ref_file:
        json.dump(ref_fournisseur, ref_file)    
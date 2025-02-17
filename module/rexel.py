import pandas as pd
import json

def used_colonnes(config_file, nom_fournisseur):
    return ",".join([key for key, val in config_file['fournisseur'][nom_fournisseur]["colonne"].items()])

def dict_reference(config_file, nom_fournisseur):
    with open('data/ref_' + nom_fournisseur + '.json') as ref_file:
        return json.load(ref_file)

def read_data(config_file, nom_fournisseur):
    print(used_colonnes(config_file, nom_fournisseur))
    return pd.read_excel('export/export_' + nom_fournisseur + '.xlsx', usecols=used_colonnes(config_file, nom_fournisseur))

def save_ref(config_file, nom_fournisseur, ref_fournisseur):
    with open('data/ref_' + nom_fournisseur + '.json', 'w') as ref_file:
        json.dump(ref_fournisseur, ref_file)
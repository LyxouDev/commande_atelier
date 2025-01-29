from cx_Freeze import setup, Executable

setup(
    name = "Commande Atelier",
    version = "1.0",
    description = "Génération de ficchier .csv pour import dans Espace Affaire à partir des exports de devis",
    executables = [Executable("main.py", base=None)],
    options = {
        'build_exe': {
            'packages': ['pandas']
        }
    }
)
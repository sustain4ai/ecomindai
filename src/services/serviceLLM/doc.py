"""
Fonction pour charger les fichiers de documentation
"""


def load_doc(doc_path):
    """
    Charge la documentation de l'outil à afficher sur l'IHM.
    :return: Contenu de la documentation (Markdown)
    """
    with open(doc_path, "r", encoding="utf8") as f:
        return f.read()

def load_doc(doc_path):
    """
    Charge la documentation de l'outil à afficher sur l'IHM.
    :return: Contenu de la documentation (Markdown)
    """
    with open(doc_path, "r") as f:
        return f.read()

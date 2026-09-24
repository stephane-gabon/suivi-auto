from pythonforandroid.recipe import Recipe
from pythonforandroid.toolchain import current_directory

import os
import shutil
import tarfile

class ReportLabRecipe(Recipe):
version = "fe660f227cac"

# L'archive est fournie directement dans le dépôt GitHub.
url = None

depends = ["python3"]

def download_if_necessary(self):
    """
    Utilise l'archive ReportLab présente à la racine du projet
    au lieu d'effectuer un téléchargement Internet.
    """
    archive_name = "reportlab-fe660f227cac.tar.gz"

    # Racine du projet GitHub :
    # p4a-recipes/reportlab/__init__.py
    # -> p4a-recipes
    # -> projet
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )

    source_archive = os.path.join(project_root, archive_name)

    if not os.path.isfile(source_archive):
        raise RuntimeError(
            "\n"
            "ERREUR: archive ReportLab introuvable.\n"
            f"Fichier attendu : {source_archive}\n"
            "\n"
            "L'archive doit être présente à la racine du dépôt :\n"
            "reportlab-fe660f227cac.tar.gz\n"
        )

    # Répertoire où p4a attend les sources téléchargées.
    recipe_dir = self.get_dir(arch=None)

    os.makedirs(recipe_dir, exist_ok=True)

    destination = os.path.join(recipe_dir, archive_name)

    if not os.path.isfile(destination):
        print(
            "ReportLab : utilisation de l'archive locale "
            f"{source_archive}"
        )
        shutil.copy2(source_archive, destination)

    # Extraction locale de l'archive.
    source_dir = os.path.join(recipe_dir, "reportlab-source")

    if not os.path.isdir(source_dir):
        os.makedirs(source_dir, exist_ok=True)

        with tarfile.open(destination, "r:gz") as tar:
            tar.extractall(source_dir)

    print("ReportLab : archive locale préparée avec succès.")


recipe = ReportLabRecipe()

from pathlib import Path

from pythonforandroid.recipe import Recipe


class ReportLabRecipe(Recipe):
    version = "fe660f227cac"

    _recipe_dir = Path(__file__).resolve().parent

    url = f"file://{_recipe_dir / 'reportlab-fe660f227cac.tar.gz'}"

    depends = ["python3"]


recipe = ReportLabRecipe()

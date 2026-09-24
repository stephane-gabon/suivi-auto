from pythonforandroid.recipe import Recipe


class ReportLabRecipe(Recipe):
    version = "fe660f227cac"
    url = "file:///home/runner/.buildozer/reportlab-fe660f227cac.tar.gz"

    depends = ["python3"]


recipe = ReportLabRecipe()

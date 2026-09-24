from pythonforandroid.recipe import PythonRecipe


class ReportLabRecipe(PythonRecipe):
    """
    Recette ReportLab utilisant une archive officielle
    ReportLab au lieu de l'ancienne source Mercurial.
    """

    version = "5.0.1"

    url = (
        "https://www.reportlab.com/pypi/simple/reportlab/"
        "reportlab-{version}.tar.gz"
    )

    depends = [
        "python3",
    ]

    site_packages_name = "reportlab"


recipe = ReportLabRecipe()


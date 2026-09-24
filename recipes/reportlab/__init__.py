from pythonforandroid.recipe import PythonRecipe

class ReportLabRecipe(PythonRecipe):
    version = "4.4.7"


    url = (
        "https://files.pythonhosted.org/packages/source/r/"
        "reportlab/reportlab-{version}.tar.gz"
    )

    depends = ["python3", "freetype"]

    site_packages_name = "reportlab"

    call_hostpython_via_targetpython = False


    recipe = ReportLabRecipe()

